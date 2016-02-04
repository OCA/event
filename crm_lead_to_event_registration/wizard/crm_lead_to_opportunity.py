# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmLead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    event_id = fields.Many2one(
        comodel_name="event.event", string="Event to be registered in")

    @api.multi
    def action_apply(self):
        res = super(CrmLead2OpportunityPartner, self).action_apply()
        self.ensure_one()
        if not self.event_id:
            return res
        registration_model = self.env['event.registration']
        lead_ids = self.env.context.get('active_ids', [])
        for lead in self.env['crm.lead'].browse(lead_ids):
            if lead.partner_id:
                registration_model.create(
                    {
                        'event_id': self.event_id.id,
                        'partner_id': lead.partner_id.id,
                        'nb_register': 1,
                    })
        return res
