# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    event_id = fields.Many2one(string="Related event", store=True,
                               related='project_id.event_id')
