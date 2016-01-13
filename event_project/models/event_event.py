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

    @api.multi
    @api.depends('task_ids')
    def _count_tasks(self):
        for event in self:
            event.count_tasks = len(event.task_ids)

    def project_data_update(self, vals):
        recalculate = False
        if self.project_id:
            project_vals = {}
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
                return recalculate
        return False

    @api.multi
    def project_free(self, vals):
        for event in self:
            if event.project_id and vals.get('project_id') is False:
                event.project_id.write({'event_id': False})

    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)
        event.project_data_update(vals)
        if 'project_id' in vals and vals.get('project_id', False):
            event._add_followers_from_event_project()
        return event

    @api.multi
    def write(self, vals):
        self.project_free(vals)
        super(EventEvent, self).write(vals)
        for event in self:
            recalculate = event.project_data_update(vals)
            if recalculate and not self.env.context.get('no_recalculate'):
                event.project_id.project_recalculate()
        if 'project_id' in vals and vals.get('project_id', False):
            self._add_followers_from_event_project()
        return True

    def _add_followers_from_event_project(self):
        follower_obj = self.env['mail.followers']
        for event in self:
            for user in event.project_id.members:
                if (user.partner_id and user.partner_id.id not in
                        event.message_follower_ids.ids):
                    follower_obj.create({'res_model': 'event.event',
                                         'res_id': event.id,
                                         'partner_id': user.partner_id.id})
            for follower in event.project_id.message_follower_ids:
                if follower.id not in event.message_follower_ids.ids:
                    follower_obj.create({'res_model': 'event.event',
                                         'res_id': event.id,
                                         'partner_id': follower.id})
