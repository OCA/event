# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class EventEvent(models.Model):

    _inherit = "event.event"

    single_attendee_registration = fields.Boolean(
        compute="_compute_single_attendee_registration",
        readonly=False,
        store=True,
        help="Check this box to ask for a single attendee at registration",
    )

    @api.depends("event_type_id")
    def _compute_single_attendee_registration(self):
        for event in self:
            event.single_attendee_registration = (
                event.event_type_id.single_attendee_registration
            )
