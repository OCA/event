# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import logging

from psycopg2 import IntegrityError
from werkzeug.exceptions import NotFound

from odoo import _, http, tools
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.event_waitlist.controllers.main import EventWaitlistController
from odoo.addons.event_waitlist.models.event_waitlist import ACTIVE_STATES

_logger = logging.getLogger(__name__)

MAX_SEATS = 10


class WebsiteEventWaitlistController(http.Controller):
    def _waitlist_form_values(self, event, **post):
        tickets = (
            event._waitlist_joinable_tickets() if event.event_ticket_ids else False
        )
        values = {
            "event": event,
            "main_object": event,
            "tickets": tickets,
            "max_seats": MAX_SEATS,
            "form": post,
            "error": False,
        }
        if not request.env.user._is_public() and not post:
            partner = request.env.user.partner_id
            values["form"] = {
                "name": partner.name,
                "email": partner.email,
                "phone": partner.phone or partner.mobile,
            }
        return values

    @http.route(
        '/event/<model("event.event"):event>/waitlist',
        type="http",
        auth="public",
        website=True,
        methods=["GET"],
        sitemap=False,
    )
    def event_waitlist_form(self, event, ticket_id=None, **kwargs):
        if not event.sudo().waitlist_enabled:
            raise NotFound()
        values = self._waitlist_form_values(event)
        if ticket_id and str(ticket_id).isdigit():
            values["form"] = dict(values["form"], ticket_id=int(ticket_id))
        values["can_join"] = event.sudo()._waitlist_can_join()
        return request.render("website_event_waitlist.waitlist_form", values)

    @http.route(
        '/event/<model("event.event"):event>/waitlist',
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        sitemap=False,
    )
    def event_waitlist_submit(self, event, **post):
        event_sudo = event.sudo()
        if not event_sudo.waitlist_enabled:
            raise NotFound()
        values = self._waitlist_form_values(event, **post)
        values["can_join"] = True
        # Honeypot against bots: real users never see this field.
        if post.get("website_url_hp"):
            return request.redirect(event.website_url)

        error = self._waitlist_validate(event_sudo, post)
        if error:
            values["error"] = error
            values["can_join"] = event_sudo._waitlist_can_join()
            return request.render("website_event_waitlist.waitlist_form", values)

        entry_vals = self._waitlist_prepare_entry_values(event_sudo, post)
        try:
            with request.env.cr.savepoint():
                entry = request.env["event.waitlist"].sudo().create(entry_vals)
        except (ValidationError, IntegrityError) as e:
            _logger.info("Waiting list sign-up refused for event %s: %s", event.id, e)
            values["error"] = self._waitlist_error_message(event_sudo, e)
            return request.render("website_event_waitlist.waitlist_form", values)
        return request.render(
            "website_event_waitlist.waitlist_success",
            {"event": event, "entry": entry, "main_object": event},
        )

    def _waitlist_validate(self, event, post):
        name = (post.get("name") or "").strip()
        email = (post.get("email") or "").strip()
        if not name or not email:
            return _("Please enter your name and email address.")
        if not tools.email_normalize(email):
            return _("Please enter a valid email address.")
        try:
            seats = int(post.get("seats") or 1)
        except ValueError:
            seats = 0
        if seats < 1 or seats > MAX_SEATS:
            return _("Please choose between 1 and %s seats.", MAX_SEATS)
        ticket = self._waitlist_get_ticket(event, post)
        if event.event_ticket_ids and not ticket:
            return _("Please choose a ticket.")
        duplicate = (
            request.env["event.waitlist"]
            .sudo()
            .search_count(
                [
                    ("event_id", "=", event.id),
                    ("email_normalized", "=", tools.email_normalize(email)),
                    ("state", "in", ACTIVE_STATES),
                ]
            )
        )
        if duplicate:
            return self._waitlist_duplicate_message()
        if not event._waitlist_can_join(ticket or None):
            if event.waitlist_is_full:
                return _("Sorry, the waiting list is full.")
            return _("The waiting list is not open for this event (anymore).")
        return False

    def _waitlist_get_ticket(self, event, post):
        ticket_id = post.get("ticket_id")
        if not ticket_id or not str(ticket_id).isdigit():
            tickets = (
                event._waitlist_joinable_tickets() if event.event_ticket_ids else False
            )
            return tickets if tickets and len(tickets) == 1 else False
        ticket = event.event_ticket_ids.filtered(lambda t: t.id == int(ticket_id))
        return ticket or False

    def _waitlist_prepare_entry_values(self, event, post):
        ticket = self._waitlist_get_ticket(event, post)
        vals = {
            "event_id": event.id,
            "event_ticket_id": ticket.id if ticket else False,
            "name": post["name"].strip(),
            "email": post["email"].strip(),
            "phone": (post.get("phone") or "").strip() or False,
            "seats": int(post.get("seats") or 1),
            "lang": request.lang.code,
        }
        if not request.env.user._is_public():
            vals["partner_id"] = request.env.user.partner_id.id
        return vals

    def _waitlist_duplicate_message(self):
        return _(
            "This email address is already on the waiting list. "
            "Please check your inbox for our confirmation email."
        )

    def _waitlist_error_message(self, event, error):
        if isinstance(error, IntegrityError):
            return self._waitlist_duplicate_message()
        if event.waitlist_is_full:
            return _("Sorry, the waiting list is full.")
        return _("Sorry, we could not add you to the waiting list.")


class WebsiteEventWaitlistTokenController(EventWaitlistController):
    """Render the token pages inside the website layout."""

    @http.route(website=True)
    def waitlist_entry_page(self, token, **kwargs):
        return super().waitlist_entry_page(token, **kwargs)

    @http.route(website=True)
    def waitlist_entry_action(self, token, action, **kwargs):
        return super().waitlist_entry_action(token, action, **kwargs)
