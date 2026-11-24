# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventQuestionsBirthdateController(WebsiteEventController):
    def _process_attendees_form(self, event, form_details):
        """Map birthdate_date question answers to the direct registration field."""
        processed = dict(form_details)
        already_handled = {}
        for key, value in form_details.items():
            if not value or key.count("-") != 2:
                continue
            registration_index, question_type, _question_id = key.split("-", 2)
            if question_type != "birthdate_date":
                continue
            if question_type in already_handled.get(registration_index, []):
                continue
            already_handled.setdefault(registration_index, []).append(question_type)
            processed.setdefault(f"{registration_index}-{question_type}", value)
        return super()._process_attendees_form(event, processed)
