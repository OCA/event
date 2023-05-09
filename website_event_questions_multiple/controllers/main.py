# Copyright 2023 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.http import request

from odoo.addons.website_event_questions.controllers.main import WebsiteEvent


class WebsiteEvent(WebsiteEvent):
    def _process_attendees_form(self, event, form_details):
        """Process data posted from the attendee details form.
        Extracts question answers:
        - For questions of type 'multiple_choice', extracting the suggested answer id"""
        registrations = super(WebsiteEvent, self)._process_attendees_form(
            event, form_details
        )

        general_answer_ids = []
        for key, _value in form_details.items():
            if "question_multi_answer" in key:
                dummy, registration_index, question_answer = key.split("-")
                question_id, answer_id = question_answer.split("_")
                question_sudo = request.env["event.question"].browse(int(question_id))
                answer_sudo = request.env["event.question.answer"].browse(
                    int(answer_id)
                )
                answer_values = None
                if question_sudo.question_type == "multiple_choice":
                    answer_values = {
                        "question_id": int(question_id),
                        "value_text_box": answer_sudo.name,
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
