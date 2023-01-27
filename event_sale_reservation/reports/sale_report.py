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

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        if fields is None:
            fields = {}
        select_str = """ ,
            t.event_reservation_type_id as event_reservation_type_id
        """
        fields.update({"event_reservation_type_id": select_str})
        groupby += ", t.event_reservation_type_id"
        return super()._query(
            with_clause=with_clause,
            fields=fields,
            groupby=groupby,
            from_clause=from_clause,
        )
