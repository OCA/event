# Copyright 2024 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from odoo.addons.event.models.event_mail import _INTERVALS


class EventMail(models.Model):
    _inherit = "event.mail"

    interval_type = fields.Selection(
        selection_add=[("after_cancel", "After the event cancellation")],
        ondelete={"after_cancel": "cascade"},
    )

    @api.depends("event_id.stage_id")
    def _compute_scheduled_date(self):
        """When we cancel the event, we set the scheduled mail"""
        regular_schedulers = self.filtered(lambda x: x.interval_type != "after_cancel")
        res = super(EventMail, regular_schedulers)._compute_scheduled_date()
        for scheduler in self.filtered(
            lambda x: x.interval_type == "after_cancel"
            and x.event_id.stage_id.is_cancelled
        ):
            date, sign = scheduler.event_id.write_date, 1
            scheduler.scheduled_date = (
                date
                + _INTERVALS[scheduler.interval_unit](sign * scheduler.interval_nbr)
                if date
                else False
            )
        return res

    def execute(self):
        """Plan the mailings"""
        regular_schedulers = self.filtered(lambda x: x.interval_type != "after_cancel")
        res = super(EventMail, regular_schedulers).execute()
        for scheduler in self.filtered(
            lambda x: x.interval_type == "after_cancel"
            and x.event_id.stage_id.is_cancelled
        ):
            # Get only registrations cancelled from the event button
            registrations = (
                scheduler.event_id.registration_ids.filtered("cancelled_from_event")
                - scheduler.mail_registration_ids.registration_id
            )
            scheduler._create_missing_mail_registrations(registrations)
            scheduler.mail_registration_ids.execute()
            total_sent = len(
                scheduler.mail_registration_ids.filtered(lambda reg: reg.mail_sent)
            )
            scheduler.update(
                {
                    "mail_done": total_sent >= len(registrations),
                    "mail_count_done": total_sent,
                }
            )
        return res


class EventMailRegistration(models.Model):
    _inherit = "event.mail.registration"

    def execute(self):
        """We don't have a very good hooks. This is almost rewritten from the original
        just allows to send the mailing to the cancelled registrations"""
        now = fields.Datetime.now()
        regular = self.filtered(
            lambda x: x.scheduler_id.interval_type != "after_cancel"
        )
        res = super(EventMailRegistration, regular).execute()
        todo = self.filtered(
            lambda x: x.scheduler_id.interval_type == "after_cancel"
            and not x.mail_sent
            and not x.registration_id.state == "draft"
            and (x.scheduled_date and x.scheduled_date <= now)
            and x.scheduler_id.notification_type == "mail"
        )
        for reg_mail in todo:
            organizer = reg_mail.scheduler_id.event_id.organizer_id
            company = self.env.company
            author = self.env.ref("base.user_root")
            if organizer.email:
                author = organizer
            elif company.email:
                author = company.partner_id
            elif self.env.user.email:
                author = self.env.user
            email_values = {
                "author_id": author.id,
            }
            if not reg_mail.scheduler_id.template_ref.email_from:
                email_values["email_from"] = author.email_formatted
            reg_mail.scheduler_id.template_ref.send_mail(
                reg_mail.registration_id.id, email_values=email_values
            )
        todo.write({"mail_sent": True})
        return res
