# Copyright 2022 Camptocamp SA
# @author Damien Crier damien.crier@camptocamp.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class EventQuickRegistration(models.TransientModel):
    _name = "event.quick.registration"

    event_id = fields.Many2one("event.event", required=True)
    event_ticket_id = fields.Many2one("event.event.ticket", required=True)
    qty = fields.Integer(required=True)
    confirm_registration = fields.Boolean()
    email = fields.Char()
    phone = fields.Char()
    name = fields.Char()

    @api.model
    def default_get(self, fields):
        res = super(EventQuickRegistration, self).default_get(fields)
        res["event_id"] = self._context.get("active_id")
        return res

    def _get_registration_data(self):
        self.ensure_one()
        return {
            "event_id": self.event_id.id,
            "event_ticket_id": self.event_ticket_id.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "origin": _("Quick creation"),
        }

    def create_attendees(self):
        self.ensure_one()
        attendees = self.env["event.registration"].create(
            [self._get_registration_data() for i in range(self.qty)]
        )
        if self.confirm_registration:
            attendees.confirm_registration()
