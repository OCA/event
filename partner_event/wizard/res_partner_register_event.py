# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api


class ResPartnerRegisterEvent(models.TransientModel):
    _name = 'res.partner.register.event'

    event = fields.Many2one('event.event', required=True)

    def _prepare_registration(self, partner):
        return {
            'event_id': self.event.id,
            'partner_id': partner.id,
            'nb_register': 1,
            'name': partner.name,
            'email': partner.email,
            'phone': partner.phone,
            'date_open': fields.Datetime.now(),
        }

    @api.multi
    def button_register(self):
        registration_obj = self.env['event.registration']
        partner_obj = self.env['res.partner']
        for partner_id in self.env.context.get('active_ids', []):
            partner = partner_obj.browse(partner_id)
            registration_obj.create(self._prepare_registration(partner))
