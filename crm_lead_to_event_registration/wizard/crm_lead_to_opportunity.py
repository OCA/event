# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmLead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    event_id = fields.Many2one(
        comodel_name="event.event", string="Create registration in this event")

    @api.multi
    def action_apply(self):
        res = super(CrmLead2OpportunityPartner, self).action_apply()
        self.ensure_one()
        if not self.event_id:
            return res
        lead_ids = self.env.context.get('active_ids', [])
        (self.env['crm.lead'].browse(lead_ids)
         .action_generate_event_registration(self.event_id))
        return res
