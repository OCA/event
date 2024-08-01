# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models
from odoo.tools import config


class EventRegistration(models.Model):
    _inherit = "event.registration"

    state = fields.Selection(
        selection_add=[("reserved", "Reserved")], ondelete={"reserved": "set default"}
    )

    def _need_pre_reservation(self):
        return False

    def action_set_reserved(self):
        if config["test_enable"] and not self.env.context.get(
            "test_event_seat_reserve"
        ):
            return True
        self.write({"state": "reserved"})
        self.event_id._check_seats_availability()
        self.event_ticket_id._check_seats_availability()
