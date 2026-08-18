# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTypeReport(models.Model):
    _inherit = "event.type.report"

    seats_reservation_total = fields.Integer(string="Reserved seats", readonly=True)

    def _select(self, fields_=()):
        fields_ += (("seats_reservation_total", "et.seats_reservation_total"),)
        return super()._select(fields_)
