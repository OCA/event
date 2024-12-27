# Copyright 2017 Tecnativa - David Vidal
# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Related project",
        domain=[("event_id", "=", False)],
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

    def _set_event_to_linked_project(self):
        for event in self.filtered("project_id"):
            event.project_id.event_id = event.id

    _sql_constraints = [
        (
            "project_id_uniq",
            "unique(project_id)",
            "You can't link two events to the same project.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        events = super().create(vals_list)
        events._set_event_to_linked_project()
        return events

    def write(self, vals):
        # If project is removed, remove event from project
        if vals.get("project_id") is False:
            self.mapped("project_id").update({"event_id": False})
        res = super().write(vals)
        # If project is set, set event to project
        if vals.get("project_id"):
            self._set_event_to_linked_project()
        elif any([f in vals for f in self._fields_to_sync_to_project()]):
            self.mapped("project_id")._sync_from_related_event()
        return res

    @api.model
    def _fields_to_sync_to_project(self):
        fields_to_check = {
            "name",
            "date_begin",
            "date_end",
            "organizer_id",
            "note",
        }

        return fields_to_check
