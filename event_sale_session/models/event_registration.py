# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.model
    def _prepare_attendee_values(self, registration):
        data = super(EventRegistration, self)._prepare_attendee_values(
            registration)
        session_id = registration['sale_order_line_id'].session_id.id
        data.update({'session_id': session_id})
        return data
