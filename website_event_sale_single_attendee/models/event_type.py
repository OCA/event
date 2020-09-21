# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class EventType(models.Model):

    _inherit = 'event.type'

    single_attendee_registration = fields.Boolean(
        help="Ask for a single attendee at registration on the website"
    )
