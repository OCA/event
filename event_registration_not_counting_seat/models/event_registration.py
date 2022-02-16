# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    count_seat = fields.Boolean(default=True)

    @api.model
    def _prepare_attendee_values(self, registration):
        res = super()._prepare_attendee_values(registration)
        ticket = res.get("event_ticket_id", False)
        if ticket:
            count_seat = self.env["event.event.ticket"].browse(ticket).count_seat
            res.update({"count_seat": count_seat})
        return res

    @api.onchange("event_ticket_id")
    def _onchange_event_ticket_id(self):
        self.count_seat = self.event_ticket_id.count_seat
