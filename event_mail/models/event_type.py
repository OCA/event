# Copyright 2019 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class EventType(models.Model):
    _inherit = "event.type"

    def _compute_event_type_mail_ids(self):
        event_mail_template_id = self.env.company.event_mail_template_id
        for template in self:
            if (
                template.use_mail_schedule
                and not template.event_type_mail_ids
                and event_mail_template_id
            ):
                template.event_type_mail_ids = [
                    (
                        0,
                        0,
                        {
                            attribute_name: line[attribute_name]
                            if not isinstance(line[attribute_name], models.BaseModel)
                            else line[attribute_name].id
                            for attribute_name in self.env[
                                "event.type.mail"
                            ]._get_event_mail_fields_whitelist()
                        },
                    )
                    for line in event_mail_template_id.scheduler_template_ids
                ]
            else:
                template.event_type_mail_ids = [(5, 0)]
