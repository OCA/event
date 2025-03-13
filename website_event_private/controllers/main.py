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
        # for private events, check authorization
        if event.event_privacy != "public" and not request.env.user.has_group(
            "website.group_website_restricted_editor"
        ):
            # get cookie from http request
            cookie = request.httprequest.cookies.get("odoo-event-%d" % event.id)
            # check if cookie match access token
            if cookie and cookie == event.access_token:
                return True
            # if cookie does not match, get the cookie from url
            if post and post.get("access_token"):
                access_token = post.get("access_token")
                # if the cookie is correct, set the cookie accordingly and succeed
                if access_token == event.access_token:
                    request.future_response.set_cookie(
                        key="odoo-event-%d" % event.id,
                        value=access_token,
                        max_age=10 * 86400,
                        secure=True,
                        httponly=True,
                        samesite="Strict",
                    )
                    return True
                # if cookie is incorrect, do not set the cookie and fail
                else:
                    return False
        # for public event or if user is authorized, allow access
        return True
