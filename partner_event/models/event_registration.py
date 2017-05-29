# -*- coding: utf-8 -*-
# © 2014 Tecnativa S.L. - Pedro M. Baeza
# © 2015 Tecnativa S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Antonio Espinosa
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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
            partner = partner_model.search(
                [('email', '=ilike', email)], limit=1)
            event = event_model.browse(vals['event_id'])
            if partner:
                partner_id = partner.id
                vals['name'] = vals.get('name') or partner.name
                vals['phone'] = vals.get('phone') or partner.phone
            elif event.create_partner:
                # Create partner
                partner = partner_model.sudo().create(
                    self._prepare_partner(vals))
                partner_id = partner.id
            vals['partner_id'] = partner_id
        return super(EventRegistration, self).create(vals)

    @api.multi
    def partner_data_update(self, data):
        reg_data = dict((k, v) for k, v in
                        data.iteritems() if k in ['name', 'email', 'phone'])
        if reg_data:
            # Only update registration data if this event is not old
            registrations = self.filtered(
                lambda x: x.event_end_date >= fields.Datetime.now())
            registrations.write(reg_data)
