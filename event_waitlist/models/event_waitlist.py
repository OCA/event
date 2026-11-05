# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import logging
import secrets
from collections import defaultdict
from datetime import timedelta

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError

from odoo.addons.base.models.res_partner import _lang_get

_logger = logging.getLogger(__name__)

# States in which an entry is still "in the queue" (counts for duplicates and
# for the maximum waiting list length).
ACTIVE_STATES = ("waiting", "offered", "payment")


class EventWaitlist(models.Model):
    _name = "event.waitlist"
    _description = "Event Waiting List Entry"
    _order = "event_id, sequence, id"
    _rec_name = "name"

    event_id = fields.Many2one(
        "event.event",
        required=True,
        ondelete="cascade",
        index=True,
    )
    event_ticket_id = fields.Many2one(
        "event.event.ticket",
        string="Ticket",
        ondelete="cascade",
        domain="[('event_id', '=', event_id)]",
    )
    company_id = fields.Many2one(related="event_id.company_id", store=True, index=True)
    partner_id = fields.Many2one(
        "res.partner", string="Contact", index="btree_not_null"
    )
    name = fields.Char(required=True)
    email = fields.Char(required=True)
    email_normalized = fields.Char(readonly=True, index=True, copy=False)
    phone = fields.Char()
    lang = fields.Selection(
        _lang_get, string="Language", default=lambda self: self.env.lang
    )
    seats = fields.Integer(default=1, required=True)
    sequence = fields.Integer(default=lambda self: self._default_sequence(), index=True)
    position = fields.Integer(
        compute="_compute_position",
        help="Position in the queue among the entries that are still waiting.",
    )
    state = fields.Selection(
        [
            ("waiting", "Waiting"),
            ("offered", "Seat offered"),
            ("confirmed", "Registered"),
            ("expired", "Offer expired"),
            ("declined", "Declined"),
            ("cancelled", "Left the list"),
        ],
        default="waiting",
        required=True,
        index=True,
        copy=False,
    )
    offer_date = fields.Datetime(string="Offered on", readonly=True, copy=False)
    offer_deadline = fields.Datetime(string="Offer valid until", copy=False)
    access_token = fields.Char(
        copy=False, index=True, groups="event.group_event_user", readonly=True
    )
    registration_ids = fields.One2many(
        "event.registration", "waitlist_entry_id", string="Registrations"
    )
    registration_count = fields.Integer(compute="_compute_registration_count")
    note = fields.Text()

    _sql_constraints = [
        ("seats_positive", "CHECK(seats > 0)", "The number of seats must be positive."),
    ]

    def init(self):
        # Hard guarantee against duplicates, also under concurrency.
        self.env.cr.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS event_waitlist_unique_active_email
            ON event_waitlist (event_id, email_normalized)
            WHERE state IN %s
            """,
            (ACTIVE_STATES,),
        )

    # ------------------------------------------------------------------
    # Defaults / computes
    # ------------------------------------------------------------------

    @api.model
    def _default_sequence(self):
        event_id = self.env.context.get("default_event_id")
        if not event_id:
            return 10
        last = self.search(
            [("event_id", "=", event_id)], order="sequence desc", limit=1
        )
        return (last.sequence or 0) + 1

    @api.model
    def _normalize_email(self, email):
        return tools.email_normalize(email or "") or (email or "").strip().lower()

    @api.depends("state", "sequence", "event_id")
    def _compute_position(self):
        events = self.event_id
        ranks = {}
        if events:
            waiting = self.sudo().search(
                [("event_id", "in", events.ids), ("state", "=", "waiting")],
                order="event_id, sequence, id",
            )
            counters = {}
            for entry in waiting:
                counters[entry.event_id.id] = counters.get(entry.event_id.id, 0) + 1
                ranks[entry.id] = counters[entry.event_id.id]
        for entry in self:
            entry.position = ranks.get(entry._origin.id or entry.id, 0)

    def _compute_registration_count(self):
        for entry in self:
            entry.registration_count = len(entry.registration_ids)

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------

    def _check_duplicate_values(self, event_id, email_normalized, exclude_ids=()):
        """Refuse a second active entry with the same email for an event.
        Checked before writing so that users get a clear message; the unique
        index guarantees it under concurrency."""
        duplicate = self.sudo().search_count(
            [
                ("id", "not in", list(exclude_ids)),
                ("event_id", "=", event_id),
                ("email_normalized", "=", email_normalized),
                ("state", "in", ACTIVE_STATES),
            ]
        )
        if duplicate:
            event = self.env["event.event"].sudo().browse(event_id)
            raise ValidationError(
                _(
                    "%(email)s is already on the waiting list of %(event)s.",
                    email=email_normalized,
                    event=event.name,
                )
            )

    @api.constrains("event_id", "event_ticket_id")
    def _check_ticket_event(self):
        for entry in self:
            if (
                entry.event_ticket_id
                and entry.event_ticket_id.event_id != entry.event_id
            ):
                raise ValidationError(_("The ticket does not belong to this event."))

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault("access_token", secrets.token_urlsafe(32))
            vals["email_normalized"] = self._normalize_email(vals.get("email"))
            if vals.get("event_id") and vals.get("state", "waiting") in ACTIVE_STATES:
                self._check_duplicate_values(vals["event_id"], vals["email_normalized"])
            if vals.get("event_id") and "sequence" not in vals:
                last = self.sudo().search(
                    [("event_id", "=", vals["event_id"])],
                    order="sequence desc",
                    limit=1,
                )
                vals["sequence"] = (last.sequence or 0) + 1
        entries = super().create(vals_list)
        for event in entries.event_id:
            event_entries = entries.filtered(lambda e, ev=event: e.event_id == ev)
            event._waitlist_check_max_size()
            for entry in event_entries:
                event._waitlist_log(
                    _(
                        "%(name)s joined the waiting list (%(seats)s seat(s)).",
                        name=entry.name,
                        seats=entry.seats,
                    )
                )
        # Seats might be free already (e.g. entry created manually in the backend)
        entries.event_id._waitlist_process()
        entries.filtered(lambda e: e.state == "waiting")._waitlist_send_mail(
            "event_waitlist.mail_template_waitlist_joined"
        )
        return entries

    def write(self, vals):
        if "email" in vals:
            vals["email_normalized"] = self._normalize_email(vals["email"])
        if {"email", "event_id", "state"} & set(vals):
            for entry in self:
                state = vals.get("state", entry.state)
                if state in ACTIVE_STATES:
                    self._check_duplicate_values(
                        vals.get("event_id", entry.event_id.id),
                        vals.get("email_normalized", entry.email_normalized),
                        exclude_ids=entry.ids,
                    )
        return super().write(vals)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @api.model
    def _get_holding_states(self):
        """States in which an entry blocks seats for its holder."""
        return ["offered"]

    @api.model
    def _waitlist_sum_seats(self, domain, groupby):
        self.flush_model(["state", "seats", "event_id", "event_ticket_id"])
        result = defaultdict(int)
        for record, seats in self.sudo()._read_group(domain, [groupby], ["seats:sum"]):
            result[record.id] += seats or 0
        return result

    def _get_portal_url(self, action=None):
        self.ensure_one()
        base_url = self.event_id.get_base_url()
        url = f"{base_url}/event/waitlist/{self.sudo().access_token}"
        if action:
            url += f"?action={action}"
        return url

    def _waitlist_send_mail(self, template_xmlid):
        if self.env.context.get("event_waitlist_no_mail"):
            return
        template = self.env.ref(template_xmlid, raise_if_not_found=False)
        if not template or not self:
            return
        for entry in self:
            template.sudo().send_mail(
                entry.id, email_layout_xmlid="mail.mail_notification_light"
            )
        cron = self.env.ref(
            "mail.ir_cron_mail_scheduler_action", raise_if_not_found=False
        )
        if cron:
            cron.sudo()._trigger()

    def _waitlist_is_offer_expired(self):
        self.ensure_one()
        return bool(self.offer_deadline and self.offer_deadline < fields.Datetime.now())

    def _waitlist_free_seats(self):
        """Return how many seats are free for this entry (event and ticket)."""
        self.ensure_one()
        event = self.event_id
        free = []
        if event.seats_limited and event.seats_max:
            free.append(event.seats_available)
        ticket = self.event_ticket_id
        if ticket and ticket.seats_max:
            free.append(ticket.seats_available)
        return min(free) if free else float("inf")

    def _waitlist_can_be_served(self):
        """Whether a seat can still be given to this entry (dates, ticket)."""
        self.ensure_one()
        ticket = self.event_ticket_id
        if ticket and (ticket.is_expired or not ticket.is_launched):
            return False
        return True

    def _waitlist_can_auto_register(self):
        """Hook: can this entry be registered without any action of the
        attendee (e.g. free ticket)? Overridden by sale bridges."""
        self.ensure_one()
        return True

    # ------------------------------------------------------------------
    # Business actions (state changes)
    # ------------------------------------------------------------------

    def _waitlist_offer(self):
        now = fields.Datetime.now()
        for entry in self:
            event = entry.event_id
            deadline = now + timedelta(hours=max(event.waitlist_offer_hours, 1))
            if event.date_begin and deadline > event.date_begin:
                deadline = event.date_begin
            entry.write(
                {"state": "offered", "offer_date": now, "offer_deadline": deadline}
            )
            event._waitlist_log(
                _(
                    "A seat was offered to %(name)s until %(deadline)s (UTC).",
                    name=entry.name,
                    deadline=fields.Datetime.to_string(deadline),
                )
            )
        self._waitlist_send_mail("event_waitlist.mail_template_waitlist_offer")

    def _waitlist_prepare_registration_values(self):
        self.ensure_one()
        vals = {
            "event_id": self.event_id.id,
            "event_ticket_id": self.event_ticket_id.id or False,
            "partner_id": self.partner_id.id or False,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "waitlist_entry_id": self.id,
            "state": "open",
        }
        return [dict(vals) for _i in range(self.seats)]

    def _waitlist_register(self):
        """Turn the entry into confirmed registrations."""
        Registration = self.env["event.registration"].sudo()
        for entry in self:
            # Release the held seats first, then consume them with real
            # registrations in the same transaction.
            entry.write({"state": "confirmed"})
            Registration.with_context(event_waitlist_no_process=True).create(
                entry._waitlist_prepare_registration_values()
            )
            entry.event_id._waitlist_log(
                _(
                    "%(name)s moved up from the waiting list and is now registered "
                    "(%(seats)s seat(s)).",
                    name=entry.name,
                    seats=entry.seats,
                )
            )
            if not entry.event_id._waitlist_has_registration_mail():
                entry._waitlist_send_mail(
                    "event_waitlist.mail_template_waitlist_confirmed"
                )

    def _waitlist_expire(self):
        for entry in self:
            entry.write({"state": "expired"})
            entry.event_id._waitlist_log(
                _("The offer for %(name)s expired.", name=entry.name)
            )
        self._waitlist_send_mail("event_waitlist.mail_template_waitlist_expired")

    def action_accept_offer(self):
        """Attendee (or staff) accepts the offered seat.
        Return False if (one of) the offers had already expired."""
        entries = self.filtered(lambda e: e.state == "offered")
        entries.event_id._waitlist_lock()
        ok = bool(entries)
        for entry in entries:
            if entry._waitlist_is_offer_expired():
                entry._waitlist_expire()
                entry.event_id._waitlist_process()
                ok = False
                continue
            entry._waitlist_accept()
        return ok

    def _waitlist_accept(self):
        """Hook for sale bridges (payment before registration)."""
        self._waitlist_register()

    def action_decline_offer(self):
        entries = self.filtered(lambda e: e.state == "offered")
        for entry in entries:
            entry.write({"state": "declined"})
            entry.event_id._waitlist_log(
                _("%(name)s declined the offered seat.", name=entry.name)
            )
        entries.event_id._waitlist_process()
        return True

    def action_leave(self):
        entries = self.filtered(lambda e: e.state in ACTIVE_STATES)
        holding = entries.filtered(lambda e: e.state in self._get_holding_states())
        for entry in entries:
            entry.write({"state": "cancelled"})
            entry.event_id._waitlist_log(
                _("%(name)s left the waiting list.", name=entry.name)
            )
        holding.event_id._waitlist_process()
        return True

    def action_offer_now(self):
        """Backend button: offer a seat (or register) this entry right away,
        regardless of its position, if seats are free."""
        entries = self.filtered(lambda e: e.state == "waiting")
        entries.event_id._waitlist_lock()
        for entry in entries:
            if entry._waitlist_free_seats() < entry.seats:
                raise UserError(
                    _("There are not enough free seats for %(name)s.", name=entry.name)
                )
            if not entry.event_id._waitlist_can_offer():
                raise UserError(
                    _(
                        "Seats can no longer be offered for this event "
                        "(it has started or is not open for registration)."
                    )
                )
            if (
                entry.event_id.waitlist_mode == "auto"
                and entry._waitlist_can_auto_register()
            ):
                entry._waitlist_register()
            else:
                entry._waitlist_offer()
        return True

    def action_reset_to_waiting(self):
        entries = self.filtered(
            lambda e: e.state in ("expired", "declined", "cancelled")
        )
        entries.write(
            {"state": "waiting", "offer_date": False, "offer_deadline": False}
        )
        entries.event_id._waitlist_process()
        return True

    def action_view_registrations(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "event.event_registration_action"
        )
        action["domain"] = [("waitlist_entry_id", "=", self.id)]
        action["context"] = {"create": False}
        return action

    # ------------------------------------------------------------------
    # Cron
    # ------------------------------------------------------------------

    @api.model
    def _cron_process_waitlists(self):
        """Expire overdue offers and fill free seats. One commit per event so
        that a concurrency conflict on one event does not block the others."""
        now = fields.Datetime.now()
        holding = self._get_holding_states()
        overdue = self.search([("state", "in", holding), ("offer_deadline", "<", now)])
        events = overdue.event_id | self.search([("state", "=", "waiting")]).event_id
        events = events.filtered(lambda ev: ev.waitlist_enabled)
        for event in events:
            try:
                with self.env.cr.savepoint():
                    event._waitlist_lock()
                    event_overdue = self.search(
                        [
                            ("event_id", "=", event.id),
                            ("state", "in", holding),
                            ("offer_deadline", "<", now),
                        ]
                    )
                    event_overdue._waitlist_expire_overdue()
                    event._waitlist_process()
                self._waitlist_commit()
            except Exception:
                _logger.exception(
                    "Waiting list processing failed for event %s", event.id
                )
                self._waitlist_rollback()

    def _waitlist_expire_overdue(self):
        """Hook: sale bridges also cancel pending carts."""
        self._waitlist_expire()

    @api.model
    def _cron_cleanup_waitlists(self):
        """Delete waiting list entries once the event is over (GDPR)."""
        now = fields.Datetime.now()
        events = self.env["event.event"].search(
            [("waitlist_ids", "!=", False), ("date_end", "<", now)]
        )
        to_delete = self.browse()
        for event in events:
            limit = event.date_end + timedelta(
                days=max(event.waitlist_retention_days, 0)
            )
            if limit <= now:
                to_delete |= event.waitlist_ids
        if to_delete:
            _logger.info(
                "Deleting %s waiting list entries of past events", len(to_delete)
            )
            to_delete.unlink()

    def _waitlist_in_test(self):
        return tools.config["test_enable"] or self.env.registry.in_test_mode()

    def _waitlist_commit(self):
        if not self._waitlist_in_test():
            self.env.cr.commit()  # pylint: disable=invalid-commit  # pragma: no cover

    def _waitlist_rollback(self):
        # The savepoint already undid the work of the failed event; outside of
        # tests also start a fresh transaction (new snapshot) for the next one.
        if not self._waitlist_in_test():
            self.env.cr.rollback()  # pragma: no cover
