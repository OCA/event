# Copyright 2023- Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEvent(WebsiteEventController):
    # ------------------------------------------------------
    # Inherit parent routes
    # ------------------------------------------------------
    @http.route()
    def event_page(self, event, page, **post):
        if not self._check_privacy(event, **post):
            return request.redirect("/event")

        return super(WebsiteEvent, self).event_page(event, page, **post)

    @http.route()
    def event(self, event, **post):
        if not self._check_privacy(event, **post):
            return request.redirect("/event")

        return super(WebsiteEvent, self).event(event, **post)

    @http.route()
    def event_register(self, event, **post):
        if not self._check_privacy(event, **post):
            return request.redirect("/event")

        return super(WebsiteEvent, self).event_register(event, **post)

    # ------------------------------------------------------
    # Business method
    # ------------------------------------------------------
    def _check_privacy(self, event, **post):
        if event.event_privacy != "public" and not request.env.user.has_group(
            "website.group_website_restricted_editor"
        ):
            cookie = request.httprequest.cookies.get("odoo-event-%d" % event.id)
            if (
                post
                and post.get("access_token")
                and post.get("access_token") == event.access_token
            ):
                access_token = post.get("access_token")
                request.future_response.set_cookie(
                    key="odoo-event-%d" % event.id,
                    value=access_token,
                    max_age=10 * 86400,
                    secure=True,
                    httponly=True,
                    samesite="Strict",
                )
                return True
            elif cookie and cookie == event.access_token:
                return True
            else:
                return False
        return True
