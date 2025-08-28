# Copyright 2017 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# Copyright 2025 Tecnativa - Víctor Martínez
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import textwrap
from collections import defaultdict

import pytz

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_datetime
from odoo.tools.mail import html_to_inner_content

from odoo.addons.event.models.event_event import vobject


class EventSession(models.Model):
    _name = "event.session"
    _inherits = {"event.event": "event_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Event session"
    _order = "date_begin"

    active = fields.Boolean(
        default=True,
    )
    event_id = fields.Many2one(
        comodel_name="event.event",
        string="Parent Event",
        domain=[("use_sessions", "=", True)],
        ondelete="cascade",
        auto_join=True,
        index=True,
        required=True,
    )
    date_begin = fields.Datetime(
        string="Start Date",
        required=True,
    )
    date_end = fields.Datetime(
        string="End Date",
        required=True,
    )
    date_begin_located = fields.Char(
        string="Start Date Located",
        compute="_compute_date_begin_located",
    )
    date_end_located = fields.Char(
        string="End Date Located",
        compute="_compute_date_end_located",
    )
    is_ongoing = fields.Boolean(
        compute="_compute_is_ongoing",
        search="_search_is_ongoing",
    )
    is_finished = fields.Boolean(
        compute="_compute_is_finished",
        search="_search_is_finished",
    )
    is_one_day = fields.Boolean(
        compute="_compute_is_one_day",
    )
    registration_ids = fields.One2many(
        comodel_name="event.registration",
        inverse_name="session_id",
        string="Attendees",
    )
    seats_reserved = fields.Integer(
        string="Reserved Seats",
        compute="_compute_seats",
        store=True,
    )
    seats_available = fields.Integer(
        string="Available Seats",
        compute="_compute_seats",
        store=True,
    )
    seats_used = fields.Integer(
        string="Number of Participants",
        compute="_compute_seats",
        store=True,
    )
    seats_taken = fields.Integer(
        string="Number of Taken Seats",
        compute="_compute_seats",
        store=True,
    )
    event_registrations_open = fields.Boolean(
        string="Registration open",
        compute="_compute_event_registrations_open",
        compute_sudo=True,
    )
    event_registrations_sold_out = fields.Boolean(
        string="Sold Out",
        compute="_compute_event_registrations_sold_out",
        compute_sudo=True,
    )
    event_mail_ids = fields.One2many(
        comodel_name="event.mail.session",
        inverse_name="session_id",
        string="Mail Schedule",
        compute="_compute_event_mail_ids",
        store=True,
    )
    stage_id = fields.Many2one(
        comodel_name="event.stage",
        default=lambda self: self.env["event.event"]._get_default_stage_id(),
        group_expand="_read_group_expand_full",
        tracking=True,
        copy=False,
        ondelete="restrict",
    )
    kanban_state = fields.Selection(
        selection=lambda self: self.env["event.event"]
        ._fields["kanban_state"]
        .selection,
        default="normal",
        copy=False,
    )
    kanban_state_label = fields.Char(
        compute="_compute_kanban_state_label",
        store=True,
        tracking=True,
    )
    session_update = fields.Selection(
        [
            ("this", "This session"),
            ("subsequent", "This and following event sessions"),
            ("all", "All event sessions"),
        ],
        help="Choose what to do with other event sessions",
        default="this",
        store=False,
    )
    session_update_message = fields.Text(
        compute="_compute_session_update_message",
    )

    @api.depends("stage_id", "kanban_state")
    def _compute_kanban_state_label(self):
        for event in self:
            if event.kanban_state == "normal":
                event.kanban_state_label = event.stage_id.legend_normal
            elif event.kanban_state == "blocked":
                event.kanban_state_label = event.stage_id.legend_blocked
            else:
                event.kanban_state_label = event.stage_id.legend_done

    @api.depends("date_begin_located", "date_tz")
    def _compute_display_name(self):
        with_event_name = self.env.context.get("with_event_name", True)
        for rec in self:
            name = f"{rec.event_id.name}, " if with_event_name else ""
            if rec.date_begin_located:
                name += rec.date_begin_located
            if rec.date_tz != self.env.user.tz:
                name += f" ({rec.date_tz})"
            rec.display_name = name

    @api.model
    def _map_registration_state_to_seats_fields(self):
        return {
            "open": "seats_reserved",
            "done": "seats_used",
        }

    @api.depends("seats_max", "registration_ids.state", "registration_ids.active")
    def _compute_seats(self):
        """Similar to core's :meth:`event_event._compute_seats`"""
        # initialize fields to 0
        for event in self:
            event.seats_reserved = event.seats_used = event.seats_available = 0
        # Aggregate registrations by session and by state
        state_field = self._map_registration_state_to_seats_fields()
        base_vals = dict((fname, 0) for fname in state_field.values())
        results = defaultdict(lambda: defaultdict(lambda: 0))
        if self.ids:
            query = """
                SELECT session_id, state, count(session_id)
                FROM event_registration
                WHERE session_id IN %s
                AND state IN %s AND active = true
                GROUP BY session_id, state
            """
            self.env["event.registration"].flush_model(
                ["session_id", "state", "active"]
            )
            self.env.cr.execute(query, (tuple(self.ids), tuple(state_field.keys())))
            for session_id, state, num in self.env.cr.fetchall():
                results[session_id][state_field[state]] = num
        # compute seats_available and expected
        for session in self:
            session.update(results.get(session._origin.id or session.id, base_vals))
            if session.seats_max > 0:
                session.seats_available = session.seats_max - (
                    session.seats_reserved + session.seats_used
                )

            session.seats_taken = session.seats_reserved + session.seats_used

    @api.depends("date_tz", "date_begin")
    def _compute_date_begin_located(self):
        """Similar to core's :meth:`event_event._compute_date_begin_tz`"""
        for rec in self:
            if rec.date_begin:
                rec.date_begin_located = format_datetime(
                    self.env,
                    rec.date_begin,
                    tz=rec.date_tz,
                    dt_format="medium",
                )
            else:  # pragma: no cover
                rec.date_begin_located = False

    @api.depends("date_tz", "date_end")
    def _compute_date_end_located(self):
        """Similar to core's :meth:`event_event._compute_date_end_tz`"""
        for rec in self:
            if rec.date_end:
                rec.date_end_located = format_datetime(
                    self.env,
                    rec.date_end,
                    tz=rec.date_tz,
                    dt_format="medium",
                )
            else:  # pragma: no cover
                rec.date_end_located = False

    def _set_tz_context(self):
        """Similar to core's :meth:`event_event._set_tz_context`"""
        return self.with_context(**self.event_id._set_tz_context().env.context)

    @api.depends("date_begin", "date_end")
    def _compute_is_ongoing(self):
        """Similar to core's :meth:`event_event._compute_is_ongoing`"""
        now = fields.Datetime.now()
        for rec in self:
            rec.is_ongoing = rec.date_begin <= now < rec.date_end

    def _search_is_ongoing(self, operator, value):
        """Similar to core's :meth:`event_event._search_is_ongoing`"""
        if operator not in ["=", "!="]:  # pragma: no cover
            raise UserError(self.env._("This operator is not supported"))
        if not isinstance(value, bool):  # pragma: no cover
            raise UserError(self.env._("Value should be True or False (not %s)", value))
        now = fields.Datetime.now()
        if (operator == "=" and value) or (operator == "!=" and not value):
            domain = [("date_begin", "<=", now), ("date_end", ">", now)]
        else:
            domain = ["|", ("date_begin", ">", now), ("date_end", "<=", now)]
        return domain

    @api.depends("date_begin", "date_end", "date_tz")
    def _compute_is_one_day(self):
        """Similar to core's :meth:`event_event._compute_field_is_one_day`"""
        for rec in self:
            # Need to localize because it could begin late and finish early in
            # another timezone
            rec = rec._set_tz_context()
            begin_tz = fields.Datetime.context_timestamp(rec, rec.date_begin)
            end_tz = fields.Datetime.context_timestamp(rec, rec.date_end)
            rec.is_one_day = begin_tz.date() == end_tz.date()

    @api.depends("date_end")
    def _compute_is_finished(self):
        """Similar to core's :meth:`event_event._compute_is_finished`"""
        for rec in self:
            if not rec.date_end:
                rec.is_finished = False
                continue
            rec = rec._set_tz_context()
            current_datetime = fields.Datetime.context_timestamp(
                rec, fields.Datetime.now()
            )
            datetime_end = fields.Datetime.context_timestamp(rec, rec.date_end)
            rec.is_finished = datetime_end <= current_datetime

    def _search_is_finished(self, operator, value):
        """Similar to core's :meth:`event_event._search_is_finished`"""
        if operator not in ["=", "!="]:  # pragma: no cover
            raise ValueError(self.env._("This operator is not supported"))
        if not isinstance(value, bool):  # pragma: no cover
            raise ValueError(
                self.env._("Value should be True or False (not %s)", value)
            )
        now = fields.Datetime.now()
        if (operator == "=" and value) or (operator == "!=" and not value):
            domain = [("date_end", "<=", now)]
        else:
            domain = [("date_end", ">", now)]
        return domain

    @api.depends(
        "date_tz",
        "date_end",
        "event_registrations_started",
        "seats_available",
        "seats_limited",
        "seats_max",
        "event_ticket_ids.sale_available",
    )
    def _compute_event_registrations_open(self):
        """Similar to core's :meth:`event_event._compute_event_registrations_open`"""
        now = fields.Datetime.now()
        for rec in self:
            rec.event_registrations_open = (
                rec.event_registrations_started
                and (not rec.date_end or rec.date_end >= now)
                and (not rec.seats_limited or not rec.seats_max or rec.seats_available)
                and (
                    not rec.event_ticket_ids
                    or any(ticket.sale_available for ticket in rec.event_ticket_ids)
                )
            )

    @api.depends(
        "event_ticket_ids.seats_available",
        "seats_limited",
        "seats_available",
    )
    def _compute_event_registrations_sold_out(self):
        """Similar to core method:`event_event._compute_event_registrations_sold_out`"""
        for rec in self:
            rec.event_registrations_sold_out = (
                rec.seats_limited and rec.seats_max and not rec.seats_available
            ) or (
                rec.event_ticket_ids
                and all(ticket.is_sold_out for ticket in rec.event_ticket_ids)
            )

    @api.depends("event_id.event_mail_ids")
    def _compute_event_mail_ids(self):
        """Compute event mail ids from its parent event

        The email schedulers for sessions are used to track their independent states,
        but the management is done directly from the parent event.event.

        This method takes care of synchronizing the session's schedulers with those
        of their parent events.
        """
        for rec in self:
            existing_schedulers = rec.event_mail_ids.scheduler_id
            event_schedulers = rec.event_id.event_mail_ids
            # Unlink the ones no-longer in sync
            to_unlink = rec.event_mail_ids.filtered(
                lambda r, event_schedulers=event_schedulers: r.scheduler_id
                not in event_schedulers
            )
            if to_unlink:
                rec.event_mail_ids = [
                    fields.Command.unlink(scheduler.id) for scheduler in to_unlink
                ]
            # Create missing ones
            to_create = event_schedulers - existing_schedulers
            if to_create:
                rec.event_mail_ids = [
                    fields.Command.create(
                        scheduler._prepare_session_mail_scheduler_vals(rec)
                    )
                    for scheduler in to_create
                ]
                # Force recomputation of scheduled date
                rec.event_mail_ids._compute_scheduled_date()

    @api.constrains("seats_max", "seats_limited", "seats_available", "registration_ids")
    def _check_seats_availability(self, minimal_availability=0):
        """Similar to core method:`event_event._check_seats_availability`"""
        sold_out_events = []
        for session in self:
            if (
                session.seats_limited
                and session.seats_max
                and session.seats_available < minimal_availability
            ):
                sold_out_events.append(
                    self.env._(
                        '- "%(event_name)s": Missing %(nb_too_many)i seats.',
                        event_name=session.name,
                        nb_too_many=minimal_availability - session.seats_available,
                    )
                )
        if sold_out_events:
            raise ValidationError(
                self.env._("There are not enough seats available for:")
                + "\n{}\n".format("\n".join(sold_out_events))
            )

    @api.constrains("date_begin", "date_end")
    def _check_closing_date(self):
        """Similar to core method:`event_event._check_closing_date`"""
        for rec in self:
            if rec.date_end <= rec.date_begin:
                raise ValidationError(
                    self.env._(
                        "The closing date cannot be earlier than the beginning date."
                    )
                )

    def mail_attendees(
        self,
        template_id,
        force_send=False,
        filter_func=lambda self: self.state != "cancel",
    ):
        """Mail session attendees

        Similar to core's :meth:`event.models.event.mail_attendees`, but here we take
        only the session's attendees into account.
        """
        template = self.env["mail.template"].browse(template_id)
        for rec in self:
            for attendee in rec.registration_ids.filtered(filter_func):
                template.send_mail(attendee.id, force_send=force_send)

    def action_open_registrations(self):
        """Open session registrations"""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "event.act_event_registration_from_event"
        )
        action["domain"] = [("id", "in", self.registration_ids.ids)]
        action["context"] = {
            "default_event_id": self.event_id.id,
            "default_session_id": self.id,
        }
        return action

    def action_set_done(self):
        """Similar to core's :meth:`event_event.action_set_done`"""
        first_ended_stage = self.env["event.stage"].search(
            [("pipe_end", "=", True)], limit=1, order="sequence"
        )
        if first_ended_stage:
            self.stage_id = first_ended_stage

    def _get_external_description(self):
        """Similar to core's :meth:`event_event._get_external_description`"""
        self.ensure_one()
        description = html_to_inner_content(self.description)
        return textwrap.shorten(description, 1900)

    def _get_ics_file(self):
        """Similar to core's :meth:`event_event._get_ics_file`"""
        result = {}
        if not vobject:
            return result
        for rec in self:
            cal = vobject.iCalendar()
            cal_event = cal.add("vevent")
            cal_event.add("created").value = fields.Datetime.now().replace(
                tzinfo=pytz.timezone("UTC")
            )
            cal_event.add("dtstart").value = rec.date_begin.astimezone(
                pytz.timezone(rec.date_tz)
            )
            cal_event.add("dtend").value = rec.date_end.astimezone(
                pytz.timezone(rec.date_tz)
            )
            cal_event.add("summary").value = rec.name
            cal_event.add("description").value = rec._get_external_description()
            if rec.address_id:
                cal_event.add("location").value = rec.address_inline
            result[rec.id] = cal.serialize().encode("utf-8")
        return result

    @api.model_create_multi
    def create(self, vals_list):
        """Similar to core's :meth:`event_event.create`"""
        records = super().create(vals_list)
        for rec in records:
            if rec.organizer_id:
                rec.message_subscribe([rec.organizer_id.id])
        return records

    @api.model
    def _session_update_fields(self):
        """List of fields that could be synced with session_update"""
        return ["active"]

    def _compute_session_update_message(self):
        """Human readable list of fields that could be synced with session_update"""
        fnames = self._session_update_fields()
        fdescs = map(lambda fname: self._fields[fname].string, fnames)
        self.session_update_message = "\n".join(map(lambda s: f"* {s}", fdescs))

    def _sync_session_update(self, vals):
        """Handles write on multiple sessions at once from the UX"""
        update = vals.pop("session_update", "this")
        if update not in ("subsequent", "all"):
            return
        if len(self) > 1:
            raise ValidationError(
                self.env._("You cannot use session_update when writing on recordsets")
            )
        to_sync = self._session_update_fields()
        to_sync_vals = {k: v for k, v in vals.items() if k in to_sync}
        if not to_sync_vals:
            return
        domain = [("event_id", "=", self.event_id.id)]
        if update == "subsequent":
            domain.append(("date_begin", ">", self.date_begin))
        records = self.search(domain)
        records.write(to_sync_vals)

    def write(self, vals):
        # OVERRIDE to apply session_update mechanism
        self._sync_session_update(vals)
        return super().write(vals)

    @api.autovacuum
    def _gc_mark_events_done(self):
        """Move every ended sessions in the next 'ended stage'
        Similar to core's :meth:`event_event._gc_mark_events_done`
        """
        ended = self.search(
            [
                ("date_end", "<", fields.Datetime.now()),
                ("stage_id.pipe_end", "=", False),
            ]
        )
        if ended:
            ended.action_set_done()
