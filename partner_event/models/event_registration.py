# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class EventRegistration(models.Model):
    _inherit = "event.registration"

    # Restrict deletion when there's a registration
    partner_id = fields.Many2one(ondelete="restrict")

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
            # Look for a partner with that email
            email = vals.get('email').replace('%', '').replace('_', '\\_')
            partner = partner_model.search(
                [('email', '=ilike', email)], limit=1,
            )
            event = event_model.browse(vals['event_id'])
            if partner:
                vals['name'] = vals.get('name') or partner.name
                vals['phone'] = vals.get('phone') or partner.phone
            elif event.create_partner:
                # Create partner
                partner = partner_model.sudo().create(
                    self._prepare_partner(vals)
                )
            vals['partner_id'] = partner.id
        return super(EventRegistration, self).create(vals)

    @api.multi
    def partner_data_update(self, data):
        reg_fields = ['name', 'email', 'phone']
        reg_data = dict((k, v) for k, v in data.iteritems() if k in reg_fields)
        if reg_data:
            # Only update registration data if this event is not old
            registrations = self.filtered(
                lambda x: x.event_end_date >= fields.Datetime.now())
            registrations.write(reg_data)
