# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class EventType(models.Model):
    _inherit = "event.type"

    seats_available_total = fields.Char(
        string="Events available (and seats)",
        compute="_compute_event_totals",
        help="Upcoming/running events of this category (and available seats).",
    )
    crm_lead_ids = fields.One2many(
        string="Leads/Opportunities",
        comodel_name="crm.lead",
        inverse_name="event_type_id",
    )
    open_opportunities_count = fields.Integer(
        compute="_compute_opportunities_totals",
        store=True,
        help="Open opportunities for events of this category.",
    )
    seats_wanted_sum = fields.Integer(
        string="Wanted seats",
        compute="_compute_opportunities_totals",
        store=True,
        help="Sum of wanted seats in opportunities for events of this category.",
    )
    seats_wanted_total = fields.Char(
        string="Opportunities (seats)",
        compute="_compute_opportunities_totals",
        store=True,
        help="Open opportunities for events of this category (and wanted seats).",
    )

    def _events_domain(self):
        """Basic domain to get related events."""
        return [
            ("event_type_id", "in", self.ids),
            # The following domain is the same as upstream's "Upcoming/Running"
            # filter, which is the default when opening events view. It'd be
            # more correct to filter for `date_end >= fields.Datetime.now()`,
            # to exclude events that finished earlier today. However, that
            # would make the smart button display a different count than the
            # events when clicking on it, so it seems more user-friendly to
            # include these events, even if they finished earlier today.
            ("date_end", ">=", fields.Date.today()),
            ("state", "!=", "cancel"),
        ]

    def _compute_event_totals(self):
        """Get how many open events and available seats exist."""
        domain = self._events_domain()
        types_with_unlimited_seats = (
            self.env["event.event"]
            .search(
                domain + [("seats_availability", "=", "unlimited")],
            )
            .mapped("event_type_id")
        )
        results = self.env["event.event"].read_group(
            domain=domain,
            fields=["seats_available"],
            groupby=["event_type_id"],
        )
        translated_unlimited = dict(
            self.env["event.event"].fields_get(["seats_availability"])[
                "seats_availability"
            ]["selection"]
        )["unlimited"]
        totals = {group["event_type_id"][0]: group for group in results}
        for one in self:
            totals_item = totals.get(one.id, {})
            event_count = totals_item.get("event_type_id_count", 0)
            seats_sum = (
                translated_unlimited
                if one in types_with_unlimited_seats
                else totals_item.get("seats_available", "0")
            )
            one.seats_available_total = "%d (%s)" % (event_count, seats_sum)

    @api.depends(
        "crm_lead_ids.active",
        "crm_lead_ids.probability",
        "crm_lead_ids.seats_wanted",
        "crm_lead_ids.type",
    )
    def _compute_opportunities_totals(self):
        """Get how many open opportunities and wanted seats exist."""
        results = self.env["crm.lead"].read_group(
            domain=[
                ("event_type_id", "in", self.ids),
                ("type", "=", "opportunity"),
                # Ignore lost and won opportunities
                ("active", "=", True),
                ("probability", "<", "100"),
            ],
            fields=["seats_wanted"],
            groupby="event_type_id",
            orderby="id",
        )
        totals = {group["event_type_id"][0]: group for group in results}
        for one in self:
            totals_item = totals.get(one.id, {})
            oppt_count = totals_item.get("event_type_id_count", 0)
            seats_sum = totals_item.get("seats_wanted", 0)
            one.open_opportunities_count = oppt_count
            one.seats_wanted_sum = seats_sum
            one.seats_wanted_total = "%d (%d)" % (oppt_count, seats_sum)

    def action_open_events(self):
        return {
            "context": {
                "default_event_type_id": self.id,
                "search_default_upcoming": True,
            },
            "domain": [("event_type_id", "=", self.id)],
            "name": _("Events"),
            "res_model": "event.event",
            "type": "ir.actions.act_window",
            "view_mode": "kanban,calendar,tree,form,pivot",
            "view_type": "form",
        }

    def action_open_opportunities(self):
        return {
            "context": {
                "default_event_type_id": self.id,
                "default_seats_wanted": True,
                "search_default_open_opportunities": True,
            },
            "domain": [("event_type_id", "=", self.id)],
            "name": _("Opportunities"),
            "res_model": "crm.lead",
            "type": "ir.actions.act_window",
            "view_mode": "kanban,tree,graph,pivot,form,calendar,activity",
            "view_type": "form",
        }
