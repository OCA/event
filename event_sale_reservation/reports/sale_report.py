# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    event_reservation_type_id = fields.Many2one(
        comodel_name="event.type",
        readonly=True,
        string="Event reservation type",
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["event_reservation_type_id"] = "t.event_reservation_type_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """, t.event_reservation_type_id"""
        return res
