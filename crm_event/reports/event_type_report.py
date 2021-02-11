# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import sql
from odoo import api, fields, models, tools


class EventTypeReport(models.Model):
    _name = "event.type.report"
    _description = "Event categories analysis report"
    _auto = False
    _order = "name"

    name = fields.Char("Category name", readonly=True)
    events_available_count = fields.Integer(
        string="Available events count", readonly=True
    )
    event_seats_availability = fields.Selection(
        string="Seats availability",
        selection=[("limited", "Limited"), ("unlimited", "Unlimited")],
        readonly=True,
    )
    seats_limited_available = fields.Integer(
        string="Available seats in limited events", readonly=True
    )
    open_opportunities_count = fields.Integer(readonly=True)
    seats_wanted = fields.Integer(string="Wanted seats", readonly=True)

    def _query(self):
        """Composed view."""
        return sql.SQL("SELECT {} FROM {} WHERE {} GROUP BY {}").format(
            self._select(),
            self._from(),
            self._where(),
            self._groupby(),
        )

    def _select(self, fields_=()):
        """Combine fields to select.

        Arguments:
            fields_: `(("field_alias", "SUM(field_definition)"), ...)`
        """
        fields_ += (
            ("id", "et.id"),
            ("name", "et.name"),
            ("events_available_count", "COUNT(ee.*)"),
            (
                "event_seats_availability",
                """CASE WHEN 'unlimited' = ANY(ARRAY_AGG(seats_availability))
                   THEN 'unlimited' ELSE 'limited' END""",
            ),
            ("seats_limited_available", "COALESCE(SUM(ee.seats_available), 0)"),
            ("open_opportunities_count", "et.open_opportunities_count"),
            ("seats_wanted", "et.seats_wanted_sum"),
        )
        parts = []
        for alias, source in fields_:
            parts.append(sql.SQL(source + " AS ") + sql.Identifier(alias))
        result = sql.Composed(parts).join(", ")
        return result

    def _from(self, clauses=()):
        """Combine clauses to form the complete FROM clause.

        Arguments:
            clauses: `("LEFT JOIN my_table mt ON mt.other_id = other.id", ...)`
        """
        clauses = (
            ("event_type et"),
            ("LEFT JOIN event_event ee ON et.id = ee.event_type_id"),
        ) + clauses
        result = sql.Composed(map(sql.SQL, clauses)).join(" ")
        return result

    def _where(self, clauses=()):
        """Combine where clauses.

        Arguments:
            clauses: `("mt.field >= 10 OR mt.field < 0", ...)`
        """
        clauses += (
            "ee.state IS NULL OR ee.state != 'cancel'",
            "ee.date_end IS NULL OR ee.date_end >= CURRENT_DATE",
        )
        result = sql.Composed(map(sql.SQL, clauses)).join(" AND ")
        return result

    def _groupby(self, clauses=()):
        """Combine group by clauses.

        Arguments:
            clauses: `("mt.field", ...)`
        """
        clauses += ("et.id",)
        result = sql.Composed(map(sql.SQL, clauses)).join(", ")
        return result

    @api.model_cr
    def init(self):
        """(Re-)create report view."""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            sql.SQL("CREATE OR REPLACE VIEW {} AS ({})").format(
                sql.Identifier(self._table),
                self._query(),
            ),
        )
