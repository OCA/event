# Copyright 2017 Tecnativa - Sergio Teruel
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

    def _prepare_event_mail_values(self):
        self.ensure_one()
        return {
            "notification_type": self.notification_type,
            "interval_nbr": self.interval_nbr,
            "interval_unit": self.interval_unit,
            "interval_type": self.interval_type,
            "template_ref": f"{self.template_ref._name},{self.template_ref.id}",
        }


class EventMailTemplate(models.Model):
    _name = "event.mail.template"
    _description = "Scheduling templates for events"

    @api.model
    def _default_scheduler_template_ids(self):
        subscription_template = self.env.ref("event.event_subscription")
        reminder_template = self.env.ref("event.event_reminder")
        return [
            {
                "notification_type": "mail",
                "interval_unit": "now",
                "interval_type": "after_sub",
                "template_ref": f"mail.template, {subscription_template.id}",
            },
            {
                "notification_type": "mail",
                "interval_nbr": 10,
                "interval_unit": "days",
                "interval_type": "before_event",
                "template_ref": f"mail.template, {reminder_template.id}",
            },
        ]

    name = fields.Char()
    scheduler_template_ids = fields.One2many(
        comodel_name="event.mail.scheduler.template",
        inverse_name="event_mail_template_id",
        string="Mail Schedule",
        default=_default_scheduler_template_ids,
    )
