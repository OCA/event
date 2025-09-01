# Copyright 2023 David Vidal <stefan.ungureanu@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class EventSaleReport(models.Model):
    _inherit = "event.sale.report"

    event_session_id = fields.Many2one(
        comodel_name="event.session",
        string="Event Session",
        readonly=True,
    )

    def _select_clause(self, *select):
        select_clause = super()._select_clause(*select)
        select_clause += ", event_session.id as event_session_id"
        return select_clause

    def _from_clause(self, *join_):
        from_clause = super()._from_clause(*join_)
        from_clause += (
            "JOIN event_session ON event_session.id = event_registration.session_id"
        )
        return from_clause
