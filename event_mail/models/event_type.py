# Copyright 2019 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command, models


class EventType(models.Model):
    _inherit = "event.type"

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        event_mail_template_id = self.env.company.event_mail_template_id
        if event_mail_template_id:
            res.update(
                {
                    "event_type_mail_ids": [
                        Command.create(line._prepare_event_mail_values())
                        for line in event_mail_template_id.scheduler_template_ids
                    ]
                }
            )
        return res
