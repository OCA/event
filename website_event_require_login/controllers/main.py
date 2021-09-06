# Copyright 2019 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.http import request, route

from odoo.addons.website_event.controllers.main import WebsiteEventController


class RequireLoginToRegister(WebsiteEventController):
    @route()
    def registration_new(self, event, **post):
        public_user = request.env.user == request.website.user_id
        if public_user and event.website_require_login:
            return request.env["ir.ui.view"]._render_template(
                "website_event_require_login"
                ".modal_attendees_registration_login_required",
                {"event_url": event.website_url},
            )
        return super(RequireLoginToRegister, self).registration_new(event, **post)
