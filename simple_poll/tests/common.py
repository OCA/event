# -*- coding: utf-8 -*-
# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import common


class TestPollQuestionCommon(common.TransactionCase):

    def setUp(self):
        super(TestPollQuestionCommon, self).setUp()

        # Usefull models
        self.PollQuestion = self.env['poll.question']
        self.QuestionOption = self.env['question.option']
        self.PollGroup = self.env['poll.group']
        self.IrModelData = self.env['ir.model.data']
        self.IrConfigParam = self.env['ir.config_parameter']

        self.partner_id = self.env.ref('base.res_partner_1').id

        # Test Poll Questions creation
        self.simple_text_question = self.PollQuestion.create({
            'title': 'Simple Text Question',
            'type': 'simple_text',
            'end_date': fields.Datetime.now(),
            'yes_no_maybe': True,
            'option_ids': [(0, 0, {'name': 'Test Option 01'})],
        })
        self.choose_date_question = self.PollQuestion.create({
            'title': 'Choose Date Question',
            'type': 'date',
            'end_date': fields.Datetime.now(),
            'yes_no_maybe': False,
            'option_ids': [(0, 0, {
                'name_date': fields.Date.today(),
            })],
        })
        self.choose_date_time_question = self.PollQuestion.create({
            'title': 'Choose DateTime Question',
            'type': 'date_time',
            'end_date': fields.Datetime.now(),
            'yes_no_maybe': True,
            'option_ids': [(0, 0, {
                'name_datetime': fields.Datetime.now(),
            })],
        })
