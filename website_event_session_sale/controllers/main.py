# -*- coding: utf-8 -*-

from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.exceptions import UserError


class WebsiteEvent(WebsiteEventController):

    def _process_registration_details(self, details):
        ''' Process data posted from the attendee details form. '''
        registrations = super(WebsiteEvent, self)._process_registration_details(
            details
        )

        for registration in registrations:
            session_id = registration.get('session_id')

            if session_id and not isinstance(session_id, int):
                session_id = int(session_id)

            registration['session_id'] = session_id

        return registrations
