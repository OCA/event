# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class EventSession(models.Model):
    _inherit = 'event.session'

    @api.multi
    @api.depends('seats_max', 'registration_ids.state',
                 'registration_ids.qty')
    def _compute_seats(self):
        for session in self:
            if not session.event_id.registration_multi_qty:
                return super(EventSession, self)._compute_seats()
            vals = {
                'seats_unconfirmed': 0,
                'seats_reserved': 0,
                'seats_used': 0,
                'seats_available': 0,
                'seats_available_expected': 0,
            }
            registrations = self.env['event.registration'].read_group([
                ('session_id', '=', session.id),
                ('state', 'in', ['draft', 'open', 'done'])
            ], ['state', 'qty'], ['state'])
            for registration in registrations:
                if registration['state'] == 'draft':
                    vals['seats_unconfirmed'] += registration['qty']
                elif registration['state'] == 'open':
                    vals['seats_reserved'] += registration['qty']
                elif registration['state'] == 'done':
                    vals['seats_used'] += registration['qty']
            vals['seats_expected'] = (
                vals['seats_unconfirmed'] + vals['seats_reserved'] +
                vals['seats_used'])
            if session.seats_max > 0:
                vals['seats_available'] = session.seats_max - (
                    vals['seats_reserved'] + vals['seats_used'])
                vals['seats_available_expected'] = (
                    session.seats_max - vals['seats_expected'])
            session.update(vals)

    @api.multi
    @api.constrains('registration_multi_qty')
    def _check_attendees_qty(self):
        for session in self:
            if not session.event_id.registration_multi_qty and \
                    max(session.registration_ids.mapped('qty') or [0]) > 1:
                raise ValidationError(
                    _('You cannot disable this option if there are '
                      'registrations with quantities greater than one.'))
