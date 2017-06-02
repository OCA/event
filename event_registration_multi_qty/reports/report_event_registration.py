# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ReportEventRegistration(models.Model):
    """Events Analysis"""
    _inherit = "report.event.registration"

    def _sub_select(self):
        """Replace the SQL expression that gets the number of registrations."""
        select_str = super(ReportEventRegistration, self)._sub_select()
        select_str = select_str.replace('count(r.event_id)', 'sum(qty)')
        select_str = select_str.replace('count(r.id)', 'sum(qty)')
        return select_str
