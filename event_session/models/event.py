# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    session_ids = fields.One2many(
        comodel_name='event.session',
        inverse_name='event_id',
        string='Sessions',
    )
    sessions_count = fields.Integer(
        compute='_compute_sessions_count',
        string='Total event sessions',
        store=True,
    )

    @api.multi
    @api.depends('session_ids')
    def _compute_sessions_count(self):
        for event in self:
            event.sessions_count = len(event.session_ids)
