# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import frozendict


class SaleReport(models.Model):
    _inherit = "sale.report"

    event_reservation_type_id = fields.Many2one(
        comodel_name="event.type",
        readonly=True,
        string="Event reservation type",
    )

    def _query(self, with_clause="", fields=frozendict(), groupby="", from_clause=""):
        fields = dict(
            fields,
            event_reservation_type_id="""
                , t.event_reservation_type_id as event_reservation_type_id
            """,
        )
        groupby += ", t.event_reservation_type_id"
        return super()._query(with_clause, fields, groupby, from_clause)
