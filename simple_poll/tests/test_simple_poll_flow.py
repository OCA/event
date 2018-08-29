# -*- coding: utf-8 -*-
# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
from urlparse import urljoin

from odoo.addons.simple_poll.tests.common import TestPollQuestionCommon


class TestSimplePollFlow(TestPollQuestionCommon):

    def test_poll_group(self):
        group_vals = {'name': 'test_poll_group',
                      'res_partner_ids': [(6, 0, [self.partner_id])]}
        self.poll_group = self.PollGroup.create(group_vals)
        self.assertEqual(1, len(self.poll_group.res_partner_ids),
                         'Test Group has no partner')
        self.assertEqual(True, bool(
            self.poll_group.res_partner_ids.email),
            'Test Group partner has no email')

    def test_public_url(self):
        def validate_url(url):
            """ Reference: https://github.com/django/django/blob/master/django/core/validators.py """
            url_regex = re.compile(
                r'^https?://'  # http:// or https://
                # domain...
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
                r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return True if url_regex.match(url) else False

        base_url = self.IrConfigParam.get_param('web.base.url')
        url = "questions/%s?uuid=%s" % (self.simple_text_question.id, self.simple_text_question.uuid)
        full_url = urljoin(base_url, url)
        self.assertTrue(validate_url(self.simple_text_question.public_url))
        self.assertEqual(full_url, self.simple_text_question.public_url)

    def test_send_by_email(self):
        action = self.choose_date_time_question.action_poll_send()
        try:
            template_id = self.IrModelData.get_object_reference(
                'simple_poll', 'email_template_edi_poll')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = self.IrModelData.get_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        ctx = dict()
        ctx.update({
            'default_model': 'poll.question',
            'default_res_id': self.choose_date_time_question.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
        })
        self.assertDictEqual(action, {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        })
