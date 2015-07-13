# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields, exceptions, api
from openerp.tools.translate import _


class ProjectTemplateWizard(models.TransientModel):
    _name = 'project.template.wizard'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Template project',
        domain="[('state', '=', 'template')]")
    event_id = fields.Many2one(comodel_name='event.event')

    @api.one
    def project_template_duplicate(self):
        if not self.project_id:
            raise exceptions.ValidationError(
                _('Template project is required.'))
        parent_id = self.project_id.parent_id.id
        res = self.project_id.with_context(
            self.env.context, parent_id=parent_id).duplicate_template()
        self.with_context(
            {'no_recalculate': True}).event_id.project_id = res['res_id']
        self.event_id.project_id.write({
            'name': self.event_id.name,
            'date_start': self.event_id.date_begin,
            'date': self.event_id.date_begin,
            'calculation_type': 'date_end',
        })
        self.event_id.project_id.project_recalculate()
