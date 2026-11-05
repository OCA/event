# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .event_waitlist import ACTIVE_STATES


class EventEvent(models.Model):
    _inherit = "event.event"

    waitlist_enabled = fields.Boolean(
        string="Waiting List",
        help="When the event or a ticket is sold out, visitors can join a "
        "waiting list and move up automatically when a seat becomes free.",
    )
    waitlist_mode = fields.Selection(
        [
            ("offer", "Offer the seat (with deadline)"),
            ("auto", "Register automatically"),
        ],
        string="When a Seat Becomes Free",
        default="offer",
        required=True,
        help="Offer the seat: the first person receives an email and must "
        "confirm within the deadline; the seat is reserved meanwhile.\n"
        "Register automatically: the first person is registered right away "
        "and receives the normal confirmation (paid tickets are always offered).",
    )
    waitlist_offer_hours = fields.Integer(
        string="Offer Deadline (hours)",
        default=12,
        help="How long a person has to accept an offered seat. The deadline "
        "never goes beyond the start of the event.",
    )
    waitlist_max_size = fields.Integer(
        string="Maximum Waiting List Length",
        help="Maximum number of people on the waiting list. 0 = unlimited.",
    )
    waitlist_retention_days = fields.Integer(
        string="Delete Entries After (days)",
        default=7,
        help="Waiting list entries are deleted automatically this many days "
        "after the end of the event (data protection).",
    )
    waitlist_ids = fields.One2many(
        "event.waitlist", "event_id", string="Waiting List Entries"
    )
    waitlist_count = fields.Integer(
        string="Waiting List Count", compute="_compute_waitlist_count"
    )
    waitlist_seats_held = fields.Integer(
        string="Seats Held for Waiting List",
        compute="_compute_seats",
        help="Seats currently offered to people from the waiting list.",
    )
    waitlist_is_full = fields.Boolean(compute="_compute_waitlist_count")

    @api.depends("waitlist_ids.state", "waitlist_max_size")
    def _compute_waitlist_count(self):
        data = (
            self.env["event.waitlist"]
            .sudo()
            ._read_group(
                [("event_id", "in", self.ids), ("state", "in", ACTIVE_STATES)],
                ["event_id"],
                ["__count"],
            )
        )
        counts = {event.id: count for event, count in data}
        for event in self:
            event.waitlist_count = counts.get(event._origin.id or event.id, 0)
            event.waitlist_is_full = bool(
                event.waitlist_max_size
                and event.waitlist_count >= event.waitlist_max_size
            )

    # ------------------------------------------------------------------
    # Seats: seats offered to the waiting list are not available to others
    # ------------------------------------------------------------------

    def _waitlist_held_seats_by(self, groupby):
        """Return {id: held seats} grouped by 'event_id' or 'event_ticket_id'."""
        Waitlist = self.env["event.waitlist"].sudo()
        ignore = self.env.context.get("event_waitlist_ignore_entry_ids") or ()
        domain = [
            ("event_id", "in", self._origin.ids if groupby == "event_id" else []),
            ("state", "in", Waitlist._get_holding_states()),
        ]
        if ignore:
            domain.append(("id", "not in", list(ignore)))
        return Waitlist._waitlist_sum_seats(domain, groupby)

    @api.depends("waitlist_ids.state", "waitlist_ids.seats")
    @api.depends_context("event_waitlist_ignore_entry_ids")
    def _compute_seats(self):
        res = super()._compute_seats()
        held = self._waitlist_held_seats_by("event_id") if self._origin.ids else {}
        for event in self:
            seats = held.get(event._origin.id, 0)
            event.waitlist_seats_held = seats
            if seats and event.seats_max > 0:
                event.seats_available -= seats
        return res

    @api.constrains(
        "waitlist_offer_hours", "waitlist_max_size", "waitlist_retention_days"
    )
    def _check_waitlist_values(self):
        for event in self:
            if event.waitlist_offer_hours < 1:
                raise ValidationError(_("The offer deadline must be at least 1 hour."))
            if event.waitlist_max_size < 0 or event.waitlist_retention_days < 0:
                raise ValidationError(_("Waiting list values cannot be negative."))

    # ------------------------------------------------------------------
    # CRUD hooks
    # ------------------------------------------------------------------

    def write(self, vals):
        res = super().write(vals)
        if {
            "seats_max",
            "seats_limited",
            "waitlist_enabled",
            "waitlist_mode",
            "date_begin",
        } & set(vals):
            self._waitlist_process()
        return res

    # ------------------------------------------------------------------
    # Waiting list engine
    # ------------------------------------------------------------------

    def _waitlist_log(self, body):
        for event in self:
            event.sudo().message_post(
                body=body,
                subtype_xmlid="mail.mt_note",
                author_id=self.env.ref("base.partner_root").id,
            )

    def _waitlist_has_registration_mail(self):
        """True when the event already sends a confirmation after each
        registration, so we do not send a second one."""
        self.ensure_one()
        return any(
            scheduler.interval_type == "after_sub"
            and scheduler.notification_type == "mail"
            and scheduler.template_ref
            for scheduler in self.sudo().event_mail_ids
        )

    def _waitlist_check_max_size(self):
        for event in self:
            if not event.waitlist_max_size:
                continue
            count = (
                self.env["event.waitlist"]
                .sudo()
                .search_count(
                    [("event_id", "=", event.id), ("state", "in", ACTIVE_STATES)]
                )
            )
            if count > event.waitlist_max_size:
                raise ValidationError(
                    _("The waiting list of %(event)s is full.", event=event.name)
                )

    def _waitlist_lock(self):
        """Serialize waiting list processing per event.

        We *update* the event rows (not only SELECT FOR UPDATE): with
        REPEATABLE READ isolation a concurrent transaction that also processes
        the same event then fails with a serialization error and is retried by
        Odoo, re-reading the committed state. This makes it impossible to
        offer/register the same person twice or to give away more seats than
        are free when two cancellations happen at the same time.
        """
        ids = self._origin.ids
        if not ids:
            return
        self.flush_recordset()
        # Bumping write_date also refreshes the website's t-cache of the
        # event page (sold out / waiting list buttons).
        self.env.cr.execute(
            """UPDATE event_event
               SET write_date = (clock_timestamp() AT TIME ZONE 'UTC')
               WHERE id IN %s""",
            (tuple(ids),),
        )
        self.invalidate_recordset(["write_date"])

    def _waitlist_can_offer(self):
        """No offers once the event has started or registrations are over."""
        self.ensure_one()
        now = fields.Datetime.now()
        if not self.waitlist_enabled or not self.active:
            return False
        # date_end is never before date_begin, so checking the start is enough
        if self.date_begin and self.date_begin <= now:
            return False
        if self.event_ticket_ids and all(t.is_expired for t in self.event_ticket_ids):
            return False
        return True

    def _waitlist_joinable_tickets(self):
        """Tickets of this event for which people may join the waiting list."""
        self.ensure_one()
        return self.event_ticket_ids.filtered(
            lambda t: not t.is_expired and t.is_launched and t.is_sold_out
        )

    def _waitlist_can_join(self, ticket=None):
        """Whether a visitor may join the waiting list (optionally for a ticket)."""
        self.ensure_one()
        if not self._waitlist_can_offer() or self.waitlist_is_full:
            return False
        if self.event_ticket_ids:
            joinable = self._waitlist_joinable_tickets()
            return ticket in joinable if ticket else bool(joinable)
        return bool(self.event_registrations_sold_out)

    def _waitlist_next_entry(self):
        """First waiting entry (in order) for which enough seats are free.
        Entries asking for more seats than available keep their position."""
        self.ensure_one()
        entries = (
            self.env["event.waitlist"]
            .sudo()
            .search(
                [("event_id", "=", self.id), ("state", "=", "waiting")],
                order="sequence, id",
            )
        )
        for entry in entries:
            if not entry._waitlist_can_be_served():
                continue
            if entry._waitlist_free_seats() >= entry.seats:
                return entry
        return entries.browse()

    def _waitlist_process(self):
        """Give free seats to the waiting list, according to the event mode."""
        if self.env.context.get("event_waitlist_no_process"):
            return
        # Lock (and refresh the website cache of) every touched event, also
        # when its waiting list was just switched off.
        self.sudo()._waitlist_lock()
        events = self.sudo().filtered(lambda ev: ev.waitlist_enabled)
        if not events:
            return
        events = events.with_context(event_waitlist_no_process=True)
        for event in events:
            if not event._waitlist_can_offer():
                continue
            # Safety net against endless loops
            for _i in range(1000):
                self.env.flush_all()
                self.env.invalidate_all()
                entry = event._waitlist_next_entry()
                if not entry:
                    break
                if (
                    event.waitlist_mode == "auto"
                    and entry._waitlist_can_auto_register()
                ):
                    entry._waitlist_register()
                else:
                    entry._waitlist_offer()

    def action_waitlist_process(self):
        """Backend button 'Move up now'."""
        self.with_context(event_waitlist_no_process=False)._waitlist_process()
        return True

    def action_view_waitlist(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "event_waitlist.event_waitlist_action"
        )
        action["domain"] = [("event_id", "=", self.id)]
        action["context"] = {
            "default_event_id": self.id,
            "search_default_filter_active": 1,
        }
        action["name"] = _("Waiting List: %s", self.name)
        return action


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    waitlist_seats_held = fields.Integer(
        string="Seats Held for Waiting List", compute="_compute_seats"
    )

    @api.depends("event_id.waitlist_ids.state", "event_id.waitlist_ids.seats")
    @api.depends_context("event_waitlist_ignore_entry_ids")
    def _compute_seats(self):
        res = super()._compute_seats()
        held = {}
        if self._origin.ids:
            Waitlist = self.env["event.waitlist"].sudo()
            ignore = self.env.context.get("event_waitlist_ignore_entry_ids") or ()
            domain = [
                ("event_ticket_id", "in", self._origin.ids),
                ("state", "in", Waitlist._get_holding_states()),
            ]
            if ignore:
                domain.append(("id", "not in", list(ignore)))
            held = Waitlist._waitlist_sum_seats(domain, "event_ticket_id")
        for ticket in self:
            seats = held.get(ticket._origin.id, 0)
            ticket.waitlist_seats_held = seats
            if seats and ticket.seats_max > 0:
                ticket.seats_available -= seats
        return res

    def write(self, vals):
        res = super().write(vals)
        if "seats_max" in vals:
            self.event_id._waitlist_process()
        return res
