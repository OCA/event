# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _action_send_mail(self, auto_commit=False):
        """Advance stage automatically if possible."""
        result = super()._action_send_mail(auto_commit)
        if (
            not self.env.context.get("auto_advance_stage")
            or self.env.context.get("active_model") != "crm.lead"
        ):
            return result
        leads = self.env["crm.lead"].browse(self.env.context.get("active_ids"))
        for lead in leads:
            if not lead.stage_id.auto_advance_stage_invite_website_event_type:
                continue
            next_stage = lead._stage_find(
                domain=[("sequence", ">", lead.stage_id.sequence)]
            )
            if next_stage:
                lead.stage_id = next_stage
        return result
