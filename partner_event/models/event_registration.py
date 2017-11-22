# -*- coding: utf-8 -*-
# © 2014 Tecnativa S.L. - Pedro M. Baeza
# © 2015 Tecnativa S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Antonio Espinosa
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    partner_id = fields.Many2one(
        ondelete='restrict',
    )
    attendee_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Attendee Partner',
        ondelete='restrict',
    )

    def _prepare_partner(self, vals):
        return {
            'name': vals.get('name') or vals.get('email'),
            'email': vals.get('email', False),
            'phone': vals.get('phone', False),
        }

    @api.model
    def create(self, vals):
        if not vals.get('attendee_partner_id') and vals.get('email'):
            Partner = self.env['res.partner']
            Event = self.env['event.event']
            # Look for a partner with that email
            email = vals.get('email').replace('%', '').replace('_', '\\_')
            attendee_partner = Partner.search([
                ('email', '=ilike', email)
            ], limit=1)
            event = Event.browse(vals['event_id'])
            if attendee_partner:
                vals['name'] = vals.setdefault('name', attendee_partner.name)
                vals['phone'] = vals.setdefault(
                    'phone', attendee_partner.phone)
            elif event.create_partner:
                # Create partner
                attendee_partner = Partner.sudo().create(
                    self._prepare_partner(vals))
            vals['attendee_partner_id'] = attendee_partner.id
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
