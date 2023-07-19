# Copyright 2021 Tecnativa - Carlos Roca
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventConfigurator(models.TransientModel):
    _inherit = "event.event.configurator"

    event_use_sessions = fields.Boolean(related="event_id.use_sessions")
    event_session_id = fields.Many2one(
        string="Session",
        comodel_name="event.session",
        domain="[('event_id', '=', event_id)]",
    )

    @api.onchange("event_id")
    def _onchange_event_id_session(self):
        # Automatically set the session, if there's only one available
        # and also to clear event_session_id if it's inconsistent with the event
        event = self.event_id
        if event.session_count == 1:
            self.event_session_id = event.session_ids[0]
        elif not event.use_sessions or event != self.event_session_id.event_id:
            self.event_session_id = False
