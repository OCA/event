# Copyright 2021 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventConfigurator(models.TransientModel):
    _inherit = "event.event.configurator"

    session_id = fields.Many2one(comodel_name="event.session", string="Session")
    event_sessions_count = fields.Integer(
        comodel_name="event.session",
        related="event_id.sessions_count",
        readonly=True,
    )

    @api.onchange("event_id")
    def _onchange_event_id(self):
        """Force default session"""
        if self.event_sessions_count == 1:
            self.session_id = self.event_id.session_ids[0]
