# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    event_id = fields.Many2one(
        string="Related event", store=True, related="project_id.event_id"
    )
