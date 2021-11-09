# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class EventRegistrationGrade(models.Model):
    _name = 'event.registration.grade'
    _description = 'Event Registration Grade'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    """ Allows grading registrants for an event (ie Exam session) """

    name = fields.Char(string='Sous Module',
                       states={'close': [('readonly', True)]},
                       required=True,
                       tracking=True
                       )
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('close', 'Closed'),
    ], tracking=True, default='draft', readonly=True, string='Status')
    grade = fields.Integer(string='Grade',
                           readonly=True,
                           states={'draft': [('readonly', False)]},
                           required=True,
                           tracking=True
                           )
    event_registration_id = fields.Many2one('event.registration',
                                            string='Event Registration')
    partner_id = fields.Many2one(related='event_registration_id.attendee_partner_id')
    company_id = fields.Many2one(
        'res.company', string='Company', related='event_registration_id.company_id',
        store=True, readonly=True, states={'draft': [('readonly', False)]})

    def grade_close(self):
        for record in self:
            record.state = 'close'

    def grade_draft(self):
        for record in self:
            record.state = 'draft'
