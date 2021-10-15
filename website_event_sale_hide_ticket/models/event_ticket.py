# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class EventEventTicket(models.Model):
    _inherit = "event.event.ticket"

    show_in_website = fields.Boolean(default=True)
