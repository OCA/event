# -*- coding: utf-8 -*-
# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import uuid
from urlparse import urljoin

from odoo import _, api, fields, models
from odoo.exceptions import Warning


class PollQuestion(models.Model):
    _name = 'poll.question'
    _inherit = ['mail.thread']
    _rec_name = 'title'

    def _default_uuid(self):
        return str(uuid.uuid4())

    @api.model
    def _default_mail_scheduler_ids(self):
        return [(0, 0, {
            'interval_nbr': 2,
            'interval_unit': 'days',
            'template_id': self.env.ref(
                'simple_poll.email_reminder_template_edi_poll')
        })]

    title = fields.Char(required=True, translate=True)

    option_ids = fields.One2many(
        'question.option', 'question_id', string='Answers', required=True,
        copy=True)
    invited_partner_ids = fields.Many2many(
        'res.partner', 'poll_question_invited_partners_rel',
        'partner_id', 'question_id', string='Invited People')

    group_ids = fields.Many2many(
        'poll.group', 'poll_question_groups_rel',
        'group_id', 'question_id', string='Poll Groups')

    type = fields.Selection([
        ('date', 'Choose Date Question'),
        ('date_time', 'Choose Date Time Question'),
        ('simple_text', 'Simple Text Question')
    ], string='Type of Question', default='simple_text', required=True)

    end_date = fields.Datetime(string='End Date', required=True)

    mail_scheduler_ids = fields.One2many(
        'poll.mail.scheduler', 'poll_id', string='Mail Schedulers',
        default=lambda self: self._default_mail_scheduler_ids())

    yes_no_maybe = fields.Boolean(string='Yes/No/Maybe Poll')

    public_url = fields.Char(string='Public link',
                             compute='_compute_question_url', readonly=True)
    question_answer_ids = fields.One2many(
        'question.answer', 'question_id', string='Answers')

    uuid = fields.Char(default=lambda self: self._default_uuid())

    @api.multi
    def _compute_question_url(self):
        """ Computes a public URL for the question """
        # TODO code used from survey _compute_survey_url function
        base_url = '/' if self.env.context.get(
            'relative_url') else self.env['ir.config_parameter'].get_param(
            'web.base.url')
        for question in self:
            question.public_url = \
                urljoin(base_url,
                        "questions/%s?uuid=%s" % (self.id, question.uuid))

    def get_participant_emails(self):
        participant_emails = [
            p.email for p in self.invited_partner_ids if p.email]
        group_participant_emails = [
            p.email for g in self.group_ids
            for p in g.res_partner_ids if p.email]
        participant_emails = set(participant_emails + group_participant_emails)
        return ",".join(participant_emails)

    def get_participants(self):
        participants = [p for p in self.invited_partner_ids]
        group_participants = [
            p for g in self.group_ids for p in g.res_partner_ids]
        all_participants = set(participants + group_participants)
        return all_participants

    def get_participants_no_answer(self):
        question_answ = self.env['question.answer']
        participants = [p for p in self.invited_partner_ids if not
                        question_answ.search([
                            ('res_partner_id', '=', p.id),
                            ('question_id', '=', self.id)])]
        group_participants = [p for g in self.group_ids for p in
                              g.res_partner_ids if not question_answ.search([
                                  ('res_partner_id', '=', p.id),
                                  ('question_id', '=', self.id)])]
        all_participants = set(participants + group_participants)
        return all_participants

    @api.multi
    def action_poll_send(self):
        '''
        This function opens a window to compose an email,
        with the edi poll template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference(
                'simple_poll', 'email_template_edi_poll')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'poll.question',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.one
    def mail_participants(self, template_id, force_send=False):
        self.env['mail.template'].browse(template_id).send_mail(
            self.id, force_send=force_send)


class QuestionOptions(models.Model):
    _name = 'question.option'

    name = fields.Char(string='Text Answer', translate=True)
    name_date = fields.Date(string='Date Answer')
    name_datetime = fields.Datetime(string='Date Time Answer')
    question_id = fields.Many2one(
        'poll.question', required=True, ondelete='cascade')
    question_type = fields.Selection(
        related='question_id.type', store=True, readonly=True)


class QuestionAnswers(models.Model):
    _name = 'question.answer'

    option_id = fields.Many2one('question.option', string='Question Option')
    question_id = fields.Many2one('poll.question', string='Question')
    res_partner_id = fields.Many2one('res.partner', string='Participant')
    answer = fields.Selection(
        [
            ('1', 'Yes'),
            ('2', 'No'),
            ('3', 'Maybe')
        ], string='Yes/No/Maybe'
    )

    _sql_constraints = [(
        'answer_uniq', 'unique(option_id, question_id, res_partner_id)',
        'One user can have only one answer for specific question and option!'),
    ]

    def save_answer(self, question, pos):
        vals = {}
        partner_id = int(pos['res_partner_id'])
        for option in question.option_ids:
            answer = self.search([('question_id', '=', question.id),
                                  ('res_partner_id', '=', partner_id),
                                  ('option_id', '=', option.id)])
            if str(option.id) in pos:
                if question.yes_no_maybe:
                    vals['answer'] = pos[str(option.id)]
                else:
                    vals['answer'] = '1'
            else:
                vals['answer'] = '2'
            if answer:
                answer.write(vals)
            else:
                vals['option_id'] = option.id
                vals['question_id'] = question.id
                vals['res_partner_id'] = partner_id
                self.create(vals)


class PollGroup(models.Model):
    _name = 'poll.group'

    name = fields.Char('Group Name')
    res_partner_ids = fields.Many2many(
        'res.partner', 'poll_group_partners_rel',
        'partner_id', 'group_id', string='Group Participants')

    @api.model
    def create(self, vals):
        res = super(PollGroup, self).create(vals)
        if res.res_partner_ids:
            for partner in res.res_partner_ids:
                if not partner.email:
                    raise Warning(
                        _("You should select Participants having email"))
        return res

    @api.multi
    def write(self, vals):
        partners_ids = vals.get('res_partner_ids', False)[0][2]
        if partners_ids:
            partners = self.env['res.partner'].browse(partners_ids)
            for partner in partners:
                if not partner.email:
                    raise Warning(
                        _("You should select Participants having email"))
        res = super(PollGroup, self).write(vals)
        return res
