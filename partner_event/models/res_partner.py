# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    registrations = fields.One2many(
        string="Event registrations",
        comodel_name='event.registration', inverse_name="partner_id")
    registration_count = fields.Integer(
        string='Event registrations number', compute='_count_registration',
        store=True)
    attended_registration_count = fields.Integer(
        string='Event attended registrations number',
        compute='_count_registration', store=True)

    @api.one
    @api.depends('registrations')
    def _count_registration(self):
        self.registration_count = len(self.registrations)
        self.attended_registration_count = len(self.registrations.filtered(
            lambda x: x.state == 'done'))
