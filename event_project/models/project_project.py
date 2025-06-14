# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    event_id = fields.Many2one(
        comodel_name="event.event", string="Related event", readonly=True
    )

    def _sync_from_related_event(self):
        for record in self.filtered("event_id"):
            event = record.event_id
            record.write(
                {
                    "name": event.display_name,
                    "date_start": event.date_begin,
                    "date": event.date_end,
                    "partner_id": event.organizer_id and event.organizer_id.id or None,
                    "description": event.note,
                }
            )

    @api.model_create_multi
    def create(self, vals_list):
        projects = super().create(vals_list)
        projects._sync_from_related_event()
        return projects

    def write(self, vals):
        res = super().write(vals)
        if vals.get("event_id"):
            self._sync_from_related_event()
        return res
