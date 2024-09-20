# Copyright 2023 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.website_event_questions.controllers.main import WebsiteEvent


class WebsiteEvent(WebsiteEvent):
    def _process_attendees_form(self, event, form_details):
        """Process data posted from the attendee details form.
        Extracts question answers:
        - For both questions asked 'once_per_order' and questions asked to every attendee
        - For questions of type 'date', extracting the text answer of the attendee."""
        registrations = super(WebsiteEvent, self)._process_attendees_form(
            event, form_details
        )

        general_answer_ids = []
        for key, value in form_details.items():
            if "question_date" in key and value:
                dummy, registration_index, question_id = key.split("-")
                answer_values = None
                answer_values = {
                    "question_id": int(question_id),
                    "value_text_box": value,
                }

                if answer_values and not int(registration_index):
                    general_answer_ids.append((0, 0, answer_values))
                elif answer_values:
                    registrations[int(registration_index) - 1][
                        "registration_answer_ids"
                    ].append((0, 0, answer_values))

        for registration in registrations:
            registration["registration_answer_ids"].extend(general_answer_ids)

        return registrations
