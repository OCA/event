# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# Copyright 2019 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    event_id = fields.Many2one(
        comodel_name="event.event",
        string="Event",
        readonly=True,
    )
    session_id = fields.Many2one(
        comodel_name="event.session",
        string="Session",
        readonly=True,
    )
    event_session_count = fields.Integer(
        string="Number of event sessions", readonly=True, group_operator="avg"
    )

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        fields = dict(fields or {})
        fields.update(
            {
                "event_id": " ,min(l.event_id) as event_id",
                "session_id": " ,min(l.session_id) as session_id",
                "event_session_count": (
                    ", min(ev.sessions_count) as event_session_count"
                ),
            }
        )
        from_clause += """
            LEFT JOIN event_session es ON l.session_id = es.id
            LEFT JOIN event_event ev ON l.event_id = ev.id
        """
        groupby += """
            ,l.event_id, l.session_id, l.id
        """
        return super()._query(with_clause, fields, groupby, from_clause)
