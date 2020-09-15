# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class EventEvent(models.Model):

    _inherit = "event.event"

    single_attendee_registration = fields.Boolean(
        help="Check this box to ask for a single attendee at registration"
    )
