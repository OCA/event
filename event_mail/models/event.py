# Copyright 2017 Tecnativa - Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    @api.model
    def _default_event_mail_template_id(self):
        return self.env.company.event_mail_template_id

    event_mail_template_id = fields.Many2one(
        comodel_name="event.mail.template",
        string="Mail Template Scheduler",
        default=_default_event_mail_template_id,
    )

    @api.depends("event_mail_template_id")
    def _compute_event_mail_ids(self):
        records = self.filtered("event_mail_template_id")
        without_template = self - records
        for event in records:
            command = [(5, 0)] + [
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
                for line in event.event_mail_template_id.scheduler_template_ids
            ]
            event.event_mail_ids = command
        super(EventEvent, without_template)._compute_event_mail_ids()
