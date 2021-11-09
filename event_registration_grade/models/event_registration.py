# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, api, fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    grade_ids = fields.One2many('event.registration.grade', 'event_registration_id',
                                string='Grades')
    grade_average = fields.Float('Grade Average',
                                 compute='_compute_grade')
    grade_count = fields.Integer('Grade Count',
                                 compute='_compute_grade')
    event_type_id = fields.Many2one(related='event_id.event_type_id')

    @api.depends('grade_ids')
    def _compute_grade(self):
        for registration in self:
            registration.grade_average = len(registration.grade_ids) != 0.0 and \
                sum(registration.grade_ids.mapped('grade'))/len(registration.grade_ids) or 0.0
            registration.grade_count = len(registration.grade_ids)


    def action_send_grade_email(self):
        """ Open a window to compose an email, with the template - 'Grades report'
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref('event_registration_grade.event_registration_mail_template_grade')
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        ctx = dict(
            default_model='event.registration',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            custom_layout="mail.mail_notification_light",
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
