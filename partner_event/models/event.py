# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    create_partner = fields.Boolean(string="Create Partners in registration",
                                    default=False)

    def _add_follower(self, partner):
        follower_obj = self.env['mail.followers']
        if partner.id not in self.message_follower_ids.ids:
            follower_obj.create({'res_model': 'event.event',
                                 'res_id': self.id,
                                 'partner_id': partner.id})


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
        registration = super(EventRegistration, self).create(vals)
        if vals.get('partner_id', False) and registration.event_id:
            registration.event_id._add_follower(registration.partner_id)
        return registration

    @api.multi
    def write(self, values):
        res = super(EventRegistration, self).write(values)
        if values.get('partner_id', False):
            for registration in self:
                if registration.event_id:
                    registration.event_id._add_follower(
                        registration.partner_id)
        return res
