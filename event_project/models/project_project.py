# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    event_id = fields.Many2one(
        comodel_name="event.event", string="Related event", readonly=True
    )
