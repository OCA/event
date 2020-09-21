# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class EventEvent(models.Model):

    _inherit = "event.event"

    single_attendee_registration = fields.Boolean(
        help="Check this box to ask for a single attendee at registration"
    )

    @api.onchange('event_type_id')
    def _onchange_type(self):
        res = super()._onchange_type()
        if self.event_type_id and self.event_type_id.single_attendee_registration:
            self.single_attendee_registration = self.event_type_id.single_attendee_registration
        return res
