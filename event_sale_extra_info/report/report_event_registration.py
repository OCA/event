# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
from openerp import fields, models, tools


class ReportEventRegistration(models.Model):
    _inherit = "report.event.registration"

    commercial_partner_id = fields.Many2one(
        "res.partner",
        "Commercial partner",
        readonly=True,
    )
    event_ticket_id = fields.Many2one(
        "event.event.ticket",
        "Ticket type",
    )

    def _get_select(self):
        """Get additional SELECT part.

        :return dict:
            In this form::

                {"field_name": "table.field_definition"}
        """
        return {
            "commercial_partner_id": "r.commercial_partner_id",
            "event_ticket_id": "r.event_ticket_id",
        }

    def _get_group_by(self):
        """Get additional GROUP BY part.

        :return list:
            In this form::

                ["table.field_name", "other.field_name"]
        """
        return [
            "r.event_ticket_id",
            "r.commercial_partner_id",
        ]

    def init(self, cr):
        """Monkey-patch view definition."""
        # Get SQL
        super(ReportEventRegistration, self).init(cr)
        cr.execute("SELECT pg_get_viewdef(%s, true)", (self._table,))
        view_def = cr.fetchone()[0]

        # Inject in SELECT
        view_def = view_def.replace(
            "FROM",
            ", %s FROM" % ",".join(
                "%s AS %s" % (v, k)
                for k, v in self._get_select().iteritems()))

        # Inject in GROUP BY
        view_def = re.sub(
            r";\s*$",
            ", %s" % ",".join(self._get_group_by()),
            view_def,
            1)

        # Re-create view
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("CREATE VIEW %s AS (%s)" % (self._table, view_def))
