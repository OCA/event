# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    event_id = fields.Many2one(string="Related event", store=True,
                               related='task_id.event_id')
