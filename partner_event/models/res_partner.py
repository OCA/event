# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    registrations = fields.One2many(
        string="Event registrations",
        comodel_name='event.registration', inverse_name="partner_id")
    event_count = fields.Integer(
        string='Events',
        compute='_compute_event_count',
        help="Count of events with confirmed registrations.",
    )
    registration_count = fields.Integer(
        string='Event registrations number', compute='_count_registration',
        store=True)
    attended_registration_count = fields.Integer(
        string='Event attended registrations number',
        compute='_count_attended_registration', store=True)

    @api.multi
    @api.depends('registrations')
    def _count_registration(self):
        for partner in self:
            partner.registration_count = len(partner.registrations)

    @api.multi
    def _compute_event_count(self):
        for partner in self:
            partner.event_count = len(
                self.env["event.registration"].search([
                    ("partner_id", "child_of", partner.id),
                    ("state", "not in", ("cancel", "draft")),
                ]).mapped("event_id"))

    @api.multi
    @api.depends('registrations.state')
    def _count_attended_registration(self):
        for partner in self:
            partner.attended_registration_count = len(
                partner.registrations.filtered(lambda x: x.state == 'done'))

    @api.multi
    def write(self, data):
        res = super(ResPartner, self).write(data)
        self.mapped('registrations').partner_data_update(data)
        return res
