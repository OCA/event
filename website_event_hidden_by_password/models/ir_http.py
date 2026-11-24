# Copyright 2026 Riccardo Fiore
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import werkzeug

from odoo import models
from odoo.http import request

from ..utils import event_visitor_unlocked


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _pre_dispatch(cls, rule, args):
        """Single choke point gating every event route that resolves an
        ``event`` argument, for visitors who have not unlocked it.

        This runs before the endpoint (and before ``super()._pre_dispatch``'s
        SEO canonical 301, which would otherwise rewrite ``/event/<id>`` to
        ``/event/<real-name>-<id>`` and hand the name to anyone guessing the
        integer id). A locked visitor is sent to the slug-free gate instead.

        It is intentionally agnostic to the route's flags so it covers, with
        no add-on dependency, both the website pages (landing, register,
        custom pages, and — when those add-ons are installed — track, agenda
        and booth pages) AND the non-website iCal downloads
        (``/event/<id>/ics`` and ``website_event_track``'s
        ``/event/<id>/track/<id>/ics``), which would otherwise stream the
        event/track name, dates and venue. Managers and already-unlocked
        visitors fall through to the normal flow.
        """
        event = args.get("event")
        if (
            event is not None
            and getattr(event, "_name", None) == "event.event"
            and request.httprequest.method in ("GET", "HEAD")
        ):
            # Re-browse in the live request env. The record bound by the URL
            # converter can carry a cursor that is already closed by the time
            # we run (super()._pre_dispatch is what rebinds args to the live
            # env, and it runs after us) — notably on read-write routes such
            # as the iCal download. event.id is cached, so reading it is safe.
            # sudo is fine: the privacy flag is not secret, and it dodges an
            # AccessError on the rare unpublished-yet-private edge.
            event_sudo = request.env["event.event"].sudo().browse(event.id)
            if event_sudo.is_private and not event_visitor_unlocked(
                request.env, request.session, event_sudo
            ):
                werkzeug.exceptions.abort(
                    request.redirect(f"/event/{event.id}/private")
                )
        return super()._pre_dispatch(rule, args)
