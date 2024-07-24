# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    state = fields.Selection(
        selection_add=[("reserved", "Reserved"), ("open",)],
        ondelete={"reserved": "set default"},
    )

    def action_set_reserved(self):
        self.write({"state": "reserved"})

    def write(self, vals):
        res = super().write(vals)
        confirming = vals.get("state") == "reserved"
        if confirming:
            self.event_id._check_seats_availability()
            self.event_ticket_id._check_seats_availability()
        return res
