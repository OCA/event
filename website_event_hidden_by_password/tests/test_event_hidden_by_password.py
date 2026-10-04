# Copyright 2026 Riccardo Fiore
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import re

from odoo.tests import HttpCase, TransactionCase, tagged


class TestEventPrivateModel(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Secret DJ Night",
                "date_begin": "2099-01-01 20:00:00",
                "date_end": "2099-01-02 02:00:00",
            }
        )

    def test_defaults_public(self):
        self.assertFalse(self.event.is_private)
        self.assertFalse(self.event.access_password)
        self.assertFalse(self.event.is_access_locked)

    def test_generate_button_rotates_password(self):
        self.event.write({"is_private": True, "access_password": "INITIAL1"})
        self.event.action_generate_access_password()
        first = self.event.access_password
        self.assertTrue(first)
        self.assertNotEqual(first, "INITIAL1")
        self.event.action_generate_access_password()
        self.assertNotEqual(self.event.access_password, first)

    def test_password_check(self):
        self.event.write({"is_private": True, "access_password": "OPENSESAME"})
        self.assertTrue(self.event._is_access_password_valid("OPENSESAME"))
        self.assertFalse(self.event._is_access_password_valid("wrong"))
        self.assertFalse(self.event._is_access_password_valid(""))
        self.assertFalse(self.event._is_access_password_valid(None))

    def test_password_check_non_ascii(self):
        # Passwords may contain accents/symbols; the compare must not crash.
        self.event.write({"is_private": True, "access_password": "café ©"})
        self.assertTrue(self.event._is_access_password_valid("café ©"))
        self.assertFalse(self.event._is_access_password_valid("cafe"))

    def test_private_autogenerates_password(self):
        # Turning an event private without a password (create or write) seeds
        # one automatically, so it can never be locked with no key.
        created = self.env["event.event"].create(
            {
                "name": "Locked, auto key",
                "date_begin": "2099-01-01 20:00:00",
                "date_end": "2099-01-02 02:00:00",
                "is_private": True,
            }
        )
        self.assertTrue(created.access_password)

        self.event.write({"is_private": True})
        self.assertTrue(self.event.access_password)

    def test_private_repopulates_cleared_password(self):
        # Clearing the password on a still-private event must not leave it
        # unopenable: the invariant re-seeds one (this is why the form can drop
        # the ``required`` modifier without risking a passwordless private
        # event).
        self.event.write({"is_private": True})
        self.event.write({"access_password": False})
        self.assertTrue(self.event.access_password)

    def test_is_access_locked_redacts_for_non_managers(self):
        self.event.write({"website_published": True, "is_private": True})
        # Admin is an event manager -> not redacted.
        self.assertFalse(self.event.is_access_locked)
        # Public visitor -> redacted.
        public = self.env.ref("base.public_user")
        self.assertTrue(self.event.with_user(public).is_access_locked)

    def test_sitemap_omits_private_event(self):
        from ..controllers.main import sitemap_event_private

        public_event = self.env["event.event"].create(
            {
                "name": "Open To Everyone",
                "date_begin": "2099-01-01 20:00:00",
                "date_end": "2099-01-02 02:00:00",
                "website_published": True,
            }
        )
        self.event.write({"website_published": True, "is_private": True})
        slug = self.env["ir.http"]._slug
        locs = [entry["loc"] for entry in sitemap_event_private(self.env, None, None)]
        # The public event's named URL is in the sitemap...
        self.assertIn(f"/event/{slug(public_event)}", locs)
        # ...but the private event's (name-bearing) URL never is.
        self.assertNotIn(f"/event/{slug(self.event)}", locs)


@tagged("post_install", "-at_install")
class TestEventPrivateFlow(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.password = "GLASSHOUSE"
        cls.event = cls.env["event.event"].create(
            {
                "name": "Members Only Set",
                "date_begin": "2099-01-01 20:00:00",
                "date_end": "2099-01-02 02:00:00",
                "website_published": True,
                "is_private": True,
                "access_password": cls.password,
                "codename": "AURORA",
            }
        )
        cls.gate_url = f"/event/{cls.event.id}/private"

    def test_listing_redacts_private_event(self):
        res = self.url_open("/event")
        self.assertEqual(res.status_code, 200)
        # The redacted card links to the slug-free gate...
        self.assertIn(f"/event/{self.event.id}/private", res.text)
        # ...and leaks none of the event's details (name)...
        self.assertNotIn(self.event.name, res.text)
        # ...but does show the public codename, so visitors tell events apart.
        self.assertIn("AURORA", res.text)

    def test_gate_is_info_free(self):
        res = self.url_open(self.gate_url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("o_wevent_event_private_gate", res.text)
        # No name, no event body.
        self.assertNotIn(self.event.name, res.text)
        self.assertNotIn("o_wevent_event_main_col", res.text)

    def test_register_page_shows_wall(self):
        res = self.url_open(f"/event/{self.event.id}/register")
        self.assertEqual(res.status_code, 200)
        self.assertIn("o_wevent_event_private_gate", res.text)
        self.assertNotIn("o_wevent_event_main_col", res.text)

    def test_wrong_then_right_password(self):
        gate = self.url_open(self.gate_url)
        token = re.search(r'name="csrf_token"\s+value="([^"]+)"', gate.text).group(1)

        wrong = self.url_open(
            f"/event/{self.event.id}/unlock",
            data={
                "csrf_token": token,
                "password": "nope",
                "redirect": f"/event/{self.event.id}",
            },
        )
        self.assertIn("o_wevent_event_private_gate", wrong.text)

        right = self.url_open(
            f"/event/{self.event.id}/unlock",
            data={
                "csrf_token": token,
                "password": self.password,
                "redirect": f"/event/{self.event.id}",
            },
        )
        # Unlocked: the event page renders, no more wall.
        self.assertEqual(right.status_code, 200)
        self.assertIn("o_wevent_event_main_col", right.text)
        self.assertNotIn("o_wevent_event_private_gate", right.text)

    # -- Search loophole (issue #108) --------------------------------------
    def test_search_by_real_name_hides_private_event(self):
        # Typing the real name must not surface the event: no redacted card,
        # no link to it, no codename. (The page echoes the *typed* term back,
        # which happens to be the name — that is the visitor's own input, not
        # a leak — so we assert on the event's own markup instead.)
        res = self.url_open("/event?search=Members+Only+Set&noFuzzy=1")
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(f"/event/{self.event.id}/private", res.text)
        self.assertNotIn("o_wevent_event_redacted", res.text)
        self.assertNotIn("AURORA", res.text)

    def test_search_by_subtitle_hides_private_event(self):
        self.event.write({"subtitle": "Backroom warehouse rave"})
        res = self.url_open("/event?search=warehouse&noFuzzy=1")
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(self.event.name, res.text)
        self.assertNotIn(f"/event/{self.event.id}/private", res.text)

    def test_search_by_codename_reveals_redacted_card(self):
        # The codename is the only key into the event, and it shows up in
        # braces on a redacted card linking to the slug-free gate.
        res = self.url_open("/event?search=AURORA&noFuzzy=1")
        self.assertEqual(res.status_code, 200)
        self.assertIn(f"/event/{self.event.id}/private", res.text)
        self.assertIn("{AURORA}", res.text)
        self.assertNotIn(self.event.name, res.text)

    # -- Direct-URL / endpoint leaks ---------------------------------------
    def test_direct_url_does_not_leak_name(self):
        # Guessing the integer id must not 301 to /event/<real-name>-<id>;
        # the visitor is sent to the slug-free gate instead.
        for path in ("/event/%s", "/event/%s/register"):
            res = self.url_open(path % self.event.id, allow_redirects=False)
            self.assertIn(res.status_code, (301, 302, 303))
            location = res.headers.get("Location", "")
            self.assertTrue(location.endswith(f"/event/{self.event.id}/private"))
            self.assertNotIn("members-only-set", location.lower())

    def test_ics_download_is_gated(self):
        # The .ics holds name/date/venue/description. This is a non-website
        # route, so it exercises the same generic ir.http guard that also
        # covers website_event_track's /event/<id>/track/<id>/ics: a locked
        # visitor is bounced to the slug-free gate, never the file.
        res = self.url_open(f"/event/{self.event.id}/ics", allow_redirects=False)
        self.assertIn(res.status_code, (301, 302, 303))
        self.assertTrue(
            res.headers.get("Location", "").endswith(f"/event/{self.event.id}/private")
        )

    def test_ics_download_open_for_manager(self):
        self.authenticate("admin", "admin")
        res = self.url_open(f"/event/{self.event.id}/ics")
        self.assertEqual(res.status_code, 200)
