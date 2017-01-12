# -*- coding: utf-8 -*-
# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from openerp.tests.common import TransactionCase
from openerp.tools.safe_eval import safe_eval


class TestEmailTemplate(TransactionCase):

    def test_fields_view_get(self):
        view = self.env['mail.template'].with_context(
            {'form_view_ref': 'mass_mailing.email_template_form_minimal'}
        ).fields_view_get()
        doc = etree.XML(view['arch'])
        for node in doc.xpath("//field[@name='model_id']"):
            domain = node.get('domain')
            if domain:
                domain = safe_eval(domain)
                for n, crit in enumerate(domain):
                    if crit[0] == 'model' and crit[1] == 'in':
                        v = list(crit[2])
                        self.assertIn('event.registration', v)
