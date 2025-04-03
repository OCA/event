# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _
from odoo.http import request, route

from odoo.addons.website_event.controllers.main import WebsiteEventController


class RequireLegalToRegister(WebsiteEventController):
    @route()
    def event_registration_success(self, event, registration_ids):
        res = super().event_registration_success(event, registration_ids)
        if event.website_require_legal:
            registration_ids_list = [int(reg) for reg in registration_ids.split(",")]
            registrations = request.env["event.registration"].browse(
                registration_ids_list
            )
            for registration in registrations:
                self._log_acceptance_metadata(registration)
        return res

    def _log_acceptance_metadata(self, record):
        """Log legal terms acceptance metadata."""
        environ = request.httprequest.headers.environ
        message = _("Website legal terms acceptance metadata: <br/>%s")
        metadata = "<br/>".join(
            "{}: {}".format(val, environ.get(val))
            for val in (
                "REMOTE_ADDR",
                "HTTP_USER_AGENT",
                "HTTP_ACCEPT_LANGUAGE",
            )
        )
        record.sudo().message_post(body=message % metadata, message_type="notification")
