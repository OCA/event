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
    seats_expected = fields.Integer(string="Seats expected", readonly=True)
    seats_max = fields.Integer(
        string="Max event seats", readonly=True, group_operator="max")
    seats_available = fields.Integer(
        string='Available seats', readonly=True, group_operator="min")
    seats_available_expected = fields.Integer(
        string='Available expected seats', readonly=True, group_operator="min")
    session_count = fields.Integer(
        string="# of Event Sessions", readonly=True, group_operator="min")

    def _select(self):
        return super(ReportEventRegistration, self)._select() + """,
            MIN(r.session_id) AS session_id,
            COELESCE(MIN(es.seats_available), e.seats_available)
                AS seats_available,
            COELESCE(MAX(es.seats_available_expected),
                     e.seats_available_expected) AS seats_available_expected,
            MIN(e.sessions_count) AS session_count
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
