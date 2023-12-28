# Copyright 2023 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def action_merge(self):
        """Inject context for later intercept it when the merge process does a flush,
        and an update is launched on the partner that recomputes attendee_partner_id.
        """
        self = self.with_context(partner_event_merging=True)
        return super().action_merge()
