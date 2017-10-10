# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Related project',
        help="Project end date will be updated with event start date.",
    )
    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='event_id',
        string='Tasks',
        readonly=True,
    )
    count_tasks = fields.Integer(
        string='Task number',
        compute='_count_tasks',
    )

    @api.multi
    @api.depends('task_ids')
    def _count_tasks(self):
        for event in self:
            event.count_tasks = len(event.task_ids)

    def project_data_update(self, vals):
        """Update data in the linked project. To be called after calling
        create/write super."""
        recalculate = False
        if self.project_id:
            project_vals = {}
            if vals.get('name'):
                project_vals['name'] = self.display_name
            if vals.get('date_begin'):
                project_vals['date'] = self.date_begin
                recalculate = True
            if vals.get('project_id'):
                project_vals['event_id'] = self.id
                project_vals['calculation_type'] = 'date_end'
                project_vals['date'] = self.date_begin
                project_vals['name'] = self.display_name
                recalculate = True
            if project_vals:
                self.project_id.write(project_vals)
        return recalculate

    def _check_new_project(self, vals):
        if vals.get('project_id'):
            vals['project_id'] = self.env['project.project'].browse(
                vals['project_id']
            ).copy().id

    @api.model
    def create(self, vals):
        self._check_new_project(vals)
        event = super(EventEvent, self).create(vals)
        event.project_data_update(vals)
        return event

    @api.multi
    def write(self, vals):
        if vals.get('project_id') is not None and not vals.get('project_id'):
            self.mapped('project_id').write({'event_id': False})
        self._check_new_project(vals)
        res = super(EventEvent, self).write(vals)
        recalculate = self.project_data_update(vals)
        if recalculate and not self.env.context.get('no_recalculate'):
            self.project_id.project_recalculate()
        return res

    @api.multi
    def button_cancel(self):
        """Archive linked project when event is cancelled"""
        super(EventEvent, self).button_cancel()
        self.mapped('project_id').write({'active': False})

    @api.multi
    def button_draft(self):
        """Uncharchive linked project when event is set to draft again"""
        super(EventEvent, self).button_draft()
        if self.project_id:
            self.project_id.active = True
