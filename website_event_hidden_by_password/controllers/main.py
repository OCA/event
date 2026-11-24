# Copyright 2026 Riccardo Fiore
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import http
from odoo.fields import Domain
from odoo.http import request

from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.website_event.controllers.main import WebsiteEventController

from ..utils import SESSION_KEY, event_visitor_unlocked


def sitemap_event_private(env, rule, qs):
    """Sitemap for the ``/event/<event>`` detail route.

    Yields the published events' canonical URLs like the core default would,
    but skips private events so their real name (the slug) never appears in
    ``sitemap.xml``.
    """
    Event = env["event.event"]
    # The public sitemap env already restricts to published events via the
    # record rule; we only add the privacy exclusion.
    dom = sitemap_qs2dom(qs, "/event", Event._rec_name) & Domain(
        "is_private", "=", False
    )
    for event in Event.search(dom):
        loc = "/event/{}".format(env["ir.http"]._slug(event))
        if not qs or qs.lower() in loc.lower():
            yield {"loc": loc}


class WebsiteEventPrivate(WebsiteEventController):
    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _event_private_is_unlocked(self, event):
        """Whether the current visitor may see this (possibly private) event."""
        return event_visitor_unlocked(request.env, request.session, event)

    def _event_private_mark_unlocked(self, event):
        unlocked = request.session.get(SESSION_KEY) or []
        if event.id not in unlocked:
            # Reassign (not append in place) so the session is marked dirty.
            request.session[SESSION_KEY] = unlocked + [event.id]

    def _event_private_safe_redirect(self, event, redirect):
        """Only allow redirects back to this event's own pages."""
        prefix = f"/event/{event.id}"
        if redirect and redirect.startswith(prefix):
            return redirect
        return prefix

    def _event_private_render_gate(self, event, redirect=None, password_error=False):
        values = {
            "event": event,
            "redirect": self._event_private_safe_redirect(event, redirect),
            "password_error": password_error,
        }
        return request.render(
            "website_event_hidden_by_password.event_private_gate", values
        )

    # ------------------------------------------------------------------
    # Gated pages
    #
    # These override routed endpoints of the parent controller. The empty
    # ``@http.route()`` re-declares them as routes that inherit the parent's
    # routing config, which is the documented way to extend a routed method
    # (without it Odoo warns that the override is "not decorated by @route").
    # ------------------------------------------------------------------
    @http.route()
    def event_register(self, event, **post):
        if not self._event_private_is_unlocked(event):
            return self._event_private_render_gate(
                event, redirect=request.httprequest.path
            )
        return super().event_register(event, **post)

    @http.route()
    def event_page(self, event, page, **post):
        if not self._event_private_is_unlocked(event):
            return self._event_private_render_gate(
                event, redirect=request.httprequest.path
            )
        return super().event_page(event, page, **post)

    @http.route(
        ["""/event/<model("event.event"):event>"""],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_event_private,
        readonly=True,
    )
    def event(self, event, **post):
        # Re-declared only to swap the core ``sitemap=True`` for one that
        # omits private events (so their name never lands in sitemap.xml);
        # the behaviour is otherwise the core redirect. Locked visitors are
        # already sent to the gate by the ir.http pre-dispatch guard.
        return super().event(event, **post)

    # ------------------------------------------------------------------
    # Unlock endpoint
    # ------------------------------------------------------------------
    @http.route(
        ["/event/<int:event_id>/private"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def event_private_locked(self, event_id, **post):
        """Slug-free gate page for a private event.

        Reached from the redacted listing card. Using a plain ``<int>`` (not
        the ``<model>`` slug converter) keeps the event name out of the URL —
        otherwise Odoo would 301 to the canonical ``/event/<name>-<id>`` URL
        and leak it. Managers / already-unlocked visitors are sent straight to
        the real page.
        """
        event = request.env["event.event"].browse(event_id).sudo().exists()
        if not event or not event.is_private:
            return request.redirect("/event")
        if self._event_private_is_unlocked(event):
            return request.redirect(f"/event/{event.id}")
        return self._event_private_render_gate(event, redirect=f"/event/{event.id}")

    @http.route(
        ['/event/<model("event.event"):event>/unlock'],
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        sitemap=False,
    )
    def event_private_unlock(self, event, password=None, redirect=None, **post):
        if event.is_private and event.sudo()._is_access_password_valid(password):
            self._event_private_mark_unlocked(event)
            return request.redirect(self._event_private_safe_redirect(event, redirect))
        return self._event_private_render_gate(
            event, redirect=redirect, password_error=True
        )
