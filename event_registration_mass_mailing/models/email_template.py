# -*- coding: utf-8 -*-
# License AGPL-3: Antiun Ingenieria S.L. - Javier Iniesta
# See README.rst file on addon root folder for more details

from lxml import etree

from openerp import models, api
from openerp.tools.safe_eval import safe_eval


class EmailTemplate(models.Model):
    _inherit = 'email.template'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(EmailTemplate, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if 'arch' in res:
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='model_id']"):
                domain = node.get('domain')
                if domain:
                    domain = safe_eval(domain)
                    for n, crit in enumerate(domain):
                        if crit[0] == 'model' and crit[1] == 'in':
                            v = list(crit[2])
                            if 'event.registration' not in v:
                                v.append('event.registration')
                                domain[n] = ('model', 'in', tuple(v))
                    node.set('domain', str(domain))
            res['arch'] = etree.tostring(doc)
        return res
