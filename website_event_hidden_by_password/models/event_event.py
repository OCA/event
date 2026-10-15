# Copyright 2026 Riccardo Fiore
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import hmac
import secrets
import string

from odoo import api, fields, models
from odoo.fields import Domain

# Password alphabet: upper-case letters + digits, minus the characters that
# are easy to confuse when read aloud or copied by hand (0/O, 1/I).
_PASSWORD_ALPHABET = "".join(
    c for c in (string.ascii_uppercase + string.digits) if c not in "O0I1"
)
_PASSWORD_LENGTH = 8


class EventEvent(models.Model):
    _inherit = "event.event"

    is_private = fields.Boolean(
        string="Private",
        copy=False,
        help="Hide this event behind a password. It is redacted on the "
        "website listing and its page asks for the access password before "
        "the content is shown.",
    )
    is_access_locked = fields.Boolean(
        string="Access Locked",
        compute="_compute_is_access_locked",
        compute_sudo=False,
        help="Technical: True when this event is private and the current user "
        "is not an event manager, i.e. its details must be redacted on the "
        "website. Used by the website templates.",
    )
    access_password = fields.Char(
        copy=False,
        groups="event.group_event_user",
        help="Shared password visitors must enter to view a private event. "
        "It is a shared secret (like a webinar password), not a user "
        "account credential, so it is stored and displayed in clear text "
        "and is only readable by event managers.",
    )
    codename = fields.Char(
        copy=False,
        help="Public reference label shown under 'Private' on the redacted "
        "card, so the people you share the password with can tell which "
        "event to open. It is NOT secret: pick a hint, not the real name "
        "(e.g. 'Aurora', 'The Greenhouse').",
    )

    @api.depends("is_private")
    @api.depends_context("uid")
    def _compute_is_access_locked(self):
        is_manager = self.env.user.has_group("event.group_event_user")
        for event in self:
            event.is_access_locked = event.is_private and not is_manager

    @api.onchange("is_private")
    def _onchange_is_private(self):
        """Seed a password the first time an event is made private (UI hint)."""
        for event in self:
            if event.is_private and not event.access_password:
                event.access_password = event._generate_access_password()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("is_private") and not vals.get("access_password"):
                vals["access_password"] = self._generate_access_password()
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        # Invariant: a private event must always have an access password,
        # otherwise nobody could open it. Re-seed any private record left
        # without one — whether it was just turned private, had its password
        # cleared, or was written through the API / an import. Enforcing it
        # here (not via a view ``required``) is what keeps the password field
        # from flashing red between the Private toggle and the onchange.
        if "is_private" in vals or "access_password" in vals:
            need_password = self.filtered(
                lambda event: event.is_private and not event.access_password
            )
            for event in need_password:
                event.access_password = event._generate_access_password()
        return res

    @api.model
    def _generate_access_password(self):
        """Return a fresh random access password."""
        return "".join(
            secrets.choice(_PASSWORD_ALPHABET) for _ in range(_PASSWORD_LENGTH)
        )

    def action_generate_access_password(self):
        """Backend button: (re)generate the access password for each event."""
        for event in self:
            event.access_password = event._generate_access_password()

    def _is_access_password_valid(self, password):
        """Constant-time check of a candidate password against the event's.

        Compares UTF-8 bytes (not ``consteq``/``hmac.compare_digest`` on str,
        which raises on non-ASCII), so passwords with accents or symbols work.
        Meant to be called with ``sudo`` so the public controller can read the
        manager-only ``access_password`` field.
        """
        self.ensure_one()
        if not self.access_password or not password:
            return False
        return hmac.compare_digest(
            self.access_password.encode("utf-8"), password.encode("utf-8")
        )

    # ------------------------------------------------------------------
    # Website search hardening
    #
    # A private event must never be discoverable through the website search
    # by its real name, subtitle or venue, and must never leak its existence
    # or metadata through the search facets. For visitors it is searchable
    # ONLY by its (non-secret) codename, and then it surfaces as a redacted
    # result shown in braces — "{codename}" — exactly like the listing card.
    # Event managers keep the normal, name-based search so they can find and
    # manage their events.
    # ------------------------------------------------------------------
    @api.model
    def _search_get_detail(self, website, order, options):
        detail = super()._search_get_detail(website, order, options)
        if not self.env.user.has_group("event.group_event_user"):
            # The date / country facet badges are counted by name against
            # these domains (see WebsiteEventController.events). Excluding
            # private events here stops a visitor who types a private event's
            # real name from learning, via the badges, that it exists at all
            # or which country it is in. The main result set (base_domain) is
            # left untouched so the redacted cards and codename search keep
            # working.
            not_private = [("is_private", "=", False)]
            detail["no_date_domain"] = detail["no_date_domain"] + [not_private]
            detail["no_country_domain"] = detail["no_country_domain"] + [not_private]
        return detail

    def _search_build_domain(self, domain_list, search, fields, extra=None):
        domain = super()._search_build_domain(domain_list, search, fields, extra)
        if search and not self.env.user.has_group("event.group_event_user"):
            # Visitors: private events match ONLY their codename (never the
            # real name / subtitle / venue that `fields` + `extra` cover), and
            # non-private events never match a codename. Empty searches skip
            # this branch, so the plain listing still shows the redacted cards.
            public = domain & Domain("is_private", "=", False)
            by_codename = super()._search_build_domain(
                domain_list, search, ["codename"]
            ) & Domain("is_private", "=", True)
            domain = public | by_codename
        return domain

    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        results_data = super()._search_render_results(
            fetch_fields, mapping, icon, limit
        )
        if self.env.user.has_group("event.group_event_user"):
            return results_data
        for event, data in zip(self, results_data, strict=False):
            if not event.is_private:
                continue
            # Redact the autocomplete row: a private event surfaces only via
            # its codename (shown in braces) and links to the slug-free gate.
            # Blank every other field so the real name, venue and subtitle
            # never reach the dropdown.
            data["name"] = "{%s}" % (event.codename or self.env._("Private"))
            data["website_url"] = f"/event/{event.id}/private"
            for leaked in ("address_name", "subtitle"):
                if leaked in data:
                    data[leaked] = False
        return results_data
