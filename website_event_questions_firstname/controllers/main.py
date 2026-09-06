# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventQuestionsFirstnameController(WebsiteEventController):
    def _process_attendees_form(self, event, form_details):
        """Map firstname/lastname question answers to direct registration fields.

        The parent handles 2-part keys ({index}-{field}) as direct field writes.
        We pre-inject such keys for firstname/lastname so they follow the same
        path as name/email/phone, including deduplication across multiple
        questions of the same type.
        """
        processed = dict(form_details)
        already_handled = {}
        for key, value in form_details.items():
            if not value or key.count("-") != 2:
                continue
            registration_index, question_type, _question_id = key.split("-", 2)
            if question_type not in ("firstname", "lastname"):
                continue
            # Deduplication: only the first answer per type per registration
            if question_type in already_handled.get(registration_index, []):
                continue
            already_handled.setdefault(registration_index, []).append(question_type)
            # Inject a 2-part key so parent writes it directly to the registration
            processed.setdefault(f"{registration_index}-{question_type}", value)
        return super()._process_attendees_form(event, processed)
