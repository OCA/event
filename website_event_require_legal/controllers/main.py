# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from markupsafe import Markup

from odoo.http import request

from odoo.addons.website_event.controllers.main import WebsiteEventController


class RequireLegalToRegister(WebsiteEventController):
    def _create_attendees_from_registration_post(self, event, registration_data):
        res = super()._create_attendees_from_registration_post(event, registration_data)
        if event.website_require_legal:
            for registration in res:
                self._log_acceptance_metadata(registration)
        return res

    def _log_acceptance_metadata(self, record):
        """Log legal terms acceptance metadata."""
        environ = request.httprequest.headers.environ
        metadata = "<br/>".join(
            f"{val}: {environ.get(val)}"
            for val in (
                "REMOTE_ADDR",
                "HTTP_USER_AGENT",
                "HTTP_ACCEPT_LANGUAGE",
            )
        )
        message = Markup(
            request.env._(
                "Website legal terms acceptance metadata: <br/>%s",
                metadata,
            )
        )
        record.sudo().message_post(
            body=message, message_type="notification", subtype_xmlid="mail.mt_comment"
        )
