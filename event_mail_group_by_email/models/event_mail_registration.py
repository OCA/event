# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EventMailRegistration(models.Model):
    _inherit = "event.mail.registration"

    def _group_by_email(self):
        """Returns a list of recordsets, grouped by email address"""
        res = []
        email_to_rec_ids = {}
        for rec in self:
            reg = rec.registration_id
            email = reg.email or reg.partner_id.email
            # If there's no email, add directly to result, ungrouped
            if email:
                email_to_rec_ids.setdefault(email, []).append(rec.id)
            else:  # pragma: no cover
                res.append(rec)
        # Add groups to result
        for __, rec_ids in email_to_rec_ids.items():
            res.append(self.browse(rec_ids))
        return res

    def execute(self):
        # Override. Handle group_by_email
        if not self.env.context.get("group_by_email"):
            return super().execute()
        # Group by scheduler
        schedulers = self.mapped("scheduler_id")
        for scheduler in schedulers:
            # Scheduler mails
            mails_to_send = self.filtered(
                lambda mail: (
                    not mail.mail_sent
                    and mail.scheduler_id.id == scheduler.id
                    and mail.registration_id.state in ["open", "done"]
                    and mail.scheduler_id.notification_type == "mail"
                )
            )
            mails_grouped = mails_to_send._group_by_email()
            for mails in mails_grouped:
                scheduler.event_id._mail_attendee_group(
                    scheduler.template_id, mails.mapped("registration_id")
                )
                # Mark all as sent
                mails.write({"mail_sent": True})
