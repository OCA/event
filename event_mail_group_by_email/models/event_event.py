# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class EventEvent(models.Model):
    _inherit = "event.event"

    def _mail_attendee_group(self, template, attendees, force_send=False):
        """Send an email notification to an attendee group."""
        if not attendees:
            return False  # pragma: no cover
        main_attendee = attendees[0]
        # Send email to main attendee
        template.with_context(records=attendees).send_mail(
            main_attendee.id, force_send=force_send
        )
        # Post a note in the others
        other_attendees = attendees - main_attendee
        if other_attendees:
            reg_url = '<a href="#model=event.registration&id=%d">%s</a>'
            body = _(
                "Communication <b>%s</b> sent to attendee " "with the same email: %s."
            ) % (
                template.display_name,
                reg_url % (main_attendee.id, main_attendee.display_name),
            )
            for attendee in other_attendees:
                attendee.message_post(body=body)

    def mail_attendees(
        self,
        template_id,
        force_send=False,
        filter_func=lambda self: self.state != "cancel",
    ):
        # Override. Group by email when context key is present
        if not self.env.context.get("group_by_email"):
            return super().mail_attendees(
                template_id, force_send=force_send, filter_func=filter_func
            )
        template = self.env["mail.template"].browse(template_id)
        for event in self:
            event_attendees = event.registration_ids.filtered(filter_func)
            attendee_groups = event_attendees._group_by_email()
            for attendees in attendee_groups:
                self._mail_attendee_group(template, attendees, force_send=force_send)
