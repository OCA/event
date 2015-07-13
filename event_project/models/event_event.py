# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Related project',
        oldname='project',
        help="Project end date will be updated with event start date.")
    task_ids = fields.One2many(
        comodel_name='project.task', related='project_id.tasks',
        string='Tasks', oldname='tasks')
    work_ids = fields.One2many(
        comodel_name='project.task.work', inverse_name='event_id',
        string='Works')
    count_tasks = fields.Integer(string='Task number', compute='_count_tasks')

    @api.one
    @api.depends('task_ids')
    def _count_tasks(self):
        self.count_tasks = len(self.task_ids)

    def project_data_update(self, vals):
        if self.project_id:
            project_vals = {}
            recalculate = False
            if vals.get('name'):
                project_vals['name'] = self.name
            if vals.get('date_begin'):
                project_vals['date'] = self.date_begin
                recalculate = True
            if vals.get('project_id'):
                project_vals['event_id'] = self.id
                recalculate = True
            if project_vals:
                self.project_id.write(project_vals)
                if recalculate:
                    self.project_id.project_recalculate()
        return True

    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)
        event.project_data_update(vals)
        return event

    @api.one
    def write(self, vals):
        super(EventEvent, self).write(vals)
        if self.env.context.get('no_recalculate'):
            return True
        self.project_data_update(vals)
        return True
