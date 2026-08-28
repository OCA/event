# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from odoo.http import request

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventQuestionsAttachment(WebsiteEventController):
    def _prepare_registration_new_values(self, event, **post):
        values = super()._prepare_registration_new_values(event, **post)
        if values:
            values["max_attachment_size"] = request.env.company.max_attachment_size
        return values

    def _process_attendees_form(self, event, form_details):
        # Remove attachment keys — files are handled via request.httprequest.files
        filtered = {
            k: v
            for k, v in form_details.items()
            if not (k.count("-") == 2 and k.split("-")[1] == "attachment")
        }
        return super()._process_attendees_form(event, filtered)

    def _create_attendees_from_registration_post(self, event, registration_data):
        attendees = super()._create_attendees_from_registration_post(
            event, registration_data
        )
        self._process_registration_attachments(attendees)
        return attendees

    def _process_registration_attachments(self, attendees):
        """Create ir.attachment records from uploaded files and link them
        to the corresponding registration answers."""
        files = request.httprequest.files
        for key, file_storage in files.items():
            parts = key.split("-")
            if len(parts) != 3 or parts[1] != "attachment":
                continue
            reg_index = int(parts[0])
            question_id = int(parts[2])
            content = file_storage.read()
            if not content:
                continue
            targets = attendees if reg_index == 0 else attendees[reg_index - 1]
            for attendee in targets if reg_index == 0 else [targets]:
                attachment = (
                    request.env["ir.attachment"]
                    .sudo()
                    .create(
                        {
                            "name": file_storage.filename,
                            "datas": base64.b64encode(content).decode(),
                            "res_model": "event.registration",
                            "res_id": attendee.id,
                            "mimetype": file_storage.content_type,
                        }
                    )
                )
                attendee.sudo().write(
                    {
                        "registration_answer_ids": [
                            (
                                0,
                                0,
                                {
                                    "question_id": question_id,
                                    "value_attachment_id": attachment.id,
                                },
                            )
                        ]
                    }
                )
