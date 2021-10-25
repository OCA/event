# Copyright 2017 Tecnativa - Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EventMailSchedulerTemplate(models.Model):
    _name = "event.mail.scheduler.template"
    _inherit = "event.mail"
    _description = "Event mail scheduler template"

    event_id = fields.Many2one(required=False)
    event_mail_template_id = fields.Many2one(
        comodel_name="event.mail.template",
        string="Event Mail Template",
        required=True,
        ondelete="cascade",
    )


class EventMailTemplate(models.Model):
    _name = "event.mail.template"
    _description = "Scheduling templates for events"

    @api.model
    def _default_scheduler_template_ids(self):
        return [
            {
                "notification_type": "mail",
                "interval_unit": "now",
                "interval_type": "after_sub",
                "template_id": self.env.ref("event.event_subscription").id,
            },
            {
                "notification_type": "mail",
                "interval_nbr": 10,
                "interval_unit": "days",
                "interval_type": "before_event",
                "template_id": self.env.ref("event.event_reminder").id,
            },
        ]

    name = fields.Char()
    scheduler_template_ids = fields.One2many(
        comodel_name="event.mail.scheduler.template",
        inverse_name="event_mail_template_id",
        string="Mail Schedule",
        default=_default_scheduler_template_ids,
    )
