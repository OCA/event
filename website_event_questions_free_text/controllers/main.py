# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.website_event_questions.controllers.main import WebsiteEvent


class WebsiteEvent(WebsiteEvent):
    def _process_registration_details(self, details):
        """Add free answers to the registration"""
        registrations = super()._process_registration_details(details)
        for registration in registrations:
            free_answers = []
            for key, value in registration.items():
                if key.startswith("answer_free_text-"):
                    free_answers.append(
                        (0, 0, {"question_id": int(key[17:]), "answer": value})
                    )
            registration["free_answer_ids"] = free_answers
        return registrations
