# Copyright 2024 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    show_cancel_button = fields.Boolean(compute="_compute_show_cancel_button")

    @api.depends("stage_id")
    def _compute_show_cancel_button(self):
        """Don't show if there aren't cancel stages or if the event is done"""
        stage_id = self.env["event.stage"].search(
            [("is_cancelled", "=", True)], limit=1
        )
        for event in self:
            event.show_cancel_button = (
                not event.stage_id.is_cancelled
                and not event.stage_id.pipe_end
                and bool(stage_id)
            )

    def button_cancel(self):
        """Perform cancellation of the attendees"""
        stage_id = self.env["event.stage"].search(
            [("is_cancelled", "=", True)], limit=1
        )
        if stage_id:
            self.stage_id = stage_id
            self.registration_ids.filtered(lambda x: x.state != "cancel").with_context(
                cancelled_from_event=True,
                # Compatibility with event_registration_cancel_reason
                bypass_reason=True,
            ).action_cancel()
