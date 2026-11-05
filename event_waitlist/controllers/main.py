# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from werkzeug.exceptions import NotFound

from odoo import http
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

from ..models.event_waitlist import ACTIVE_STATES

ACTIONS = ("accept", "decline", "leave")


class EventWaitlistController(http.Controller):
    """Token based pages for people on a waiting list. No record ids are
    exposed: the random access token is the only key."""

    def _waitlist_get_entry(self, token):
        if not token or len(token) < 20:
            raise NotFound()
        entry = (
            request.env["event.waitlist"]
            .sudo()
            .search([("access_token", "=", token)], limit=1)
        )
        if not entry:
            raise NotFound()
        return entry

    def _waitlist_page_values(self, entry, **kwargs):
        return {
            "entry": entry,
            "event": entry.event_id,
            "token": entry.access_token,
            "action": kwargs.get("action")
            if kwargs.get("action") in ACTIONS
            else False,
            "message": kwargs.get("message"),
            "error": kwargs.get("error"),
            "active_states": ACTIVE_STATES,
        }

    @http.route(
        "/event/waitlist/<string:token>",
        type="http",
        auth="public",
        methods=["GET"],
        sitemap=False,
    )
    def waitlist_entry_page(self, token, **kwargs):
        entry = self._waitlist_get_entry(token)
        # Expire offers on display, so the page is always accurate even if the
        # cron has not run yet.
        if entry.state == "offered" and entry._waitlist_is_offer_expired():
            entry._waitlist_expire()
            entry.event_id._waitlist_process()
        return request.render(
            "event_waitlist.waitlist_entry_page",
            self._waitlist_page_values(entry, **kwargs),
        )

    @http.route(
        "/event/waitlist/<string:token>/<string:action>",
        type="http",
        auth="public",
        methods=["POST"],
        sitemap=False,
    )
    def waitlist_entry_action(self, token, action, **kwargs):
        # GET is never used for state changes: mail scanners follow links.
        if action not in ACTIONS:
            raise NotFound()
        entry = self._waitlist_get_entry(token)
        try:
            result = self._waitlist_do_action(entry, action)
        except (UserError, ValidationError) as e:
            request.env.cr.rollback()
            return request.render(
                "event_waitlist.waitlist_entry_page",
                self._waitlist_page_values(
                    self._waitlist_get_entry(token), error=str(e.args[0])
                ),
            )
        if result is not None:
            return result
        return request.redirect(f"/event/waitlist/{token}?message={action}")

    def _waitlist_do_action(self, entry, action):
        """Return None to redirect back to the entry page, or a response."""
        if action == "accept":
            if entry.state != "offered":
                return None
            if not entry.action_accept_offer():
                return request.redirect(
                    f"/event/waitlist/{entry.access_token}?message=expired"
                )
            return self._waitlist_after_accept(entry)
        elif action == "decline":
            entry.action_decline_offer()
        elif action == "leave":
            entry.action_leave()
        return None

    def _waitlist_after_accept(self, entry):
        """Hook: sale bridges redirect to the checkout here."""
        return
