# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, api


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _prepare_partner(self, vals):
        return {
            'name': vals.get('name') or vals.get('email'),
            'email': vals.get('email', False),
            'phone': vals.get('phone', False),
        }

    @api.model
    def create(self, vals):
        if not vals.get('partner_id') and vals.get('email'):
            partner_model = self.env['res.partner']
            event_model = self.env['event.event']
            partner_id = False
            # Look for a partner with that email
            email = vals.get('email').replace('%', '').replace('_', '\\_')
            partners = partner_model.search(
                [('email', '=ilike', email)])
            event = event_model.browse(vals['event_id'])
            if partners:
                partner_id = partners[0].id
                vals['name'] = vals.get('name') or partners[0].name
                vals['phone'] = vals.get('phone') or partners[0].phone
            elif event.create_partner:
                # Create partner
                partner = partner_model.sudo().create(
                    self._prepare_partner(vals))
                partner_id = partner.id
            vals['partner_id'] = partner_id
        return super(EventRegistration, self).create(vals)
