# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields


class Project(models.Model):
    _inherit = 'project.project'

    event_id = fields.Many2one(
        comodel_name='event.event', string="Related event", readonly=True)
