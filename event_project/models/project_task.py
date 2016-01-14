# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details
from openerp import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    event_id = fields.Many2one(string="Related event", store=True,
                               related='project_id.event_id')
