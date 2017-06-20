# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Sergio Teruel
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ReportEventRegistration(models.Model):
    """Events Analysis"""
    _inherit = "report.event.registration"

    def _select(self):
        """Replace the SQL expression that gets the number of registrations."""
        select_str = super(ReportEventRegistration, self)._select()
        return select_str.replace('count(r.event_id)', 'sum(r.qty)')
