# Copyright 2017 Tecnativa - David Vidal
# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Related project",
        help="Project end date will be updated with event start date.",
    )
    task_ids = fields.One2many(
        comodel_name="project.task",
        inverse_name="event_id",
        string="Tasks",
        readonly=True,
    )
    count_tasks = fields.Integer(
        string="Task number",
        compute="_compute_count_tasks",
    )

    @api.depends("task_ids")
    def _compute_count_tasks(self):
        for event in self:
            event.count_tasks = len(event.task_ids)

    def project_data_update(self, vals):
        """Update data in the linked project. To be called after calling
        create/write super."""

        def _get_project_vals(event):
            return {
                "name": event.display_name,
                "date_start": event.date_begin,
                "date": event.date_end,
                "event_id": event.id,
                "partner_id": event.organizer_id.id,
                "description": event.note,
            }

        fields_to_check = {
            "name",
            "date_begin",
            "date_end",
            "project_id",
            "organizer_id",
            "note",
        }
        if not any([f in vals for f in fields_to_check]):
            return

        for event in self:
            if not event.project_id:
                continue
            event.project_id.write(_get_project_vals(event))

    @api.model
    def create(self, vals):
        events = super().create(vals)
        events.project_data_update(vals)
        return events

    def write(self, vals):
        if vals.get("project_id") is False:
            self.mapped("project_id").write({"event_id": False})
        res = super().write(vals)
        self.project_data_update(vals)
        return res
