# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ReportEventRegistration(models.Model):
    """Events Analysis"""
    _inherit = "report.event.registration"

    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
        required=True,
        readonly=True,
    )
    session_seats_max = fields.Integer(
        string="Maximum session seats", readonly=True, group_operator="avg")
    session_seats_available = fields.Integer(
        string='Available session Seats', readonly=True, group_operator="avg")

    def _select(self):
        select_str = super(ReportEventRegistration, self)._select()
        return select_str + """
            , MIN(r.session_id) AS session_id,
            MIN(es.seats_max) AS session_seats_max,
            MIN(es.seats_available) AS session_seats_available
        """

    def _from(self):
        from_str = super(ReportEventRegistration, self)._from()
        from_str += """
            LEFT JOIN event_session es ON r.session_id = es.id
        """
        return from_str

    def _group_by(self):
        group_by_str = super(ReportEventRegistration, self)._group_by()
        return group_by_str + ", r.session_id"
