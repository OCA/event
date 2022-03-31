# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    count_seat = fields.Boolean(related="event_ticket_id.count_seat", store=True)
