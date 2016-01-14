# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('registrations')
    def _count_registration(self):
        for partner in self:
            partner.registration_count = len(partner.registrations)

    @api.multi
    @api.depends('registrations.state')
    def _count_attended_registration(self):
        for partner in self:
            partner.attended_registration_count = len(
                partner.registrations.filtered(lambda x: x.state == 'done'))

    registrations = fields.One2many(
        string="Event registrations",
        comodel_name='event.registration', inverse_name="partner_id")
    registration_count = fields.Integer(
        string='Event registrations number', compute='_count_registration',
        store=True)
    attended_registration_count = fields.Integer(
        string='Event attended registrations number',
        compute='_count_attended_registration', store=True)
