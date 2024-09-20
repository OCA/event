# Copyright 2023 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEvent(WebsiteEventController):
    def _create_attendees_from_registration_post(self, event, registration_data):
        """ """
        if event.unique_attendee_email:
            existing_registration_ids = event.sudo().registration_ids.filtered(
                lambda r: r.email in [data.get("email") for data in registration_data]
            )
            if event.email_duplication_behaviour == "update":
                existing_registration_ids.unlink()
                return super()._create_attendees_from_registration_post(
                    event, registration_data
                )
            else:
                attendee_emails = event.sudo().registration_ids.mapped("email")
                for data in registration_data:
                    if data.get("email") in attendee_emails:
                        registration_data.remove(data)
                created_attendee_ids = super()._create_attendees_from_registration_post(
                    event, registration_data
                )
                return created_attendee_ids + existing_registration_ids
        else:
            return super()._create_attendees_from_registration_post(
                event, registration_data
            )
