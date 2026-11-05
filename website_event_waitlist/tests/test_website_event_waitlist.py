# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import re
from datetime import timedelta
from unittest.mock import patch

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import HttpCase, tagged
from odoo.tools import mute_logger

from odoo.addons.event_waitlist.tests.common import WaitlistCommon

from ..controllers.main import WebsiteEventWaitlistController


@tagged("post_install", "-at_install")
class TestWebsiteEventWaitlist(WaitlistCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_waitlist_data(cls.env)
        cls.event.website_published = True

    def url_open(self, url, *args, **kwargs):
        self.env.flush_all()
        res = super().url_open(url, *args, **kwargs)
        self.env.invalidate_all()
        return res

    def _csrf(self, url=None):
        page = self.url_open("/web/login").text
        return re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)

    def _join(self, event=None, **data):
        url = f"/event/{(event or self.event).id}/waitlist"
        values = {
            "csrf_token": self._csrf(url),
            "name": "Web Visitor",
            "email": "web.visitor@example.com",
            "seats": "1",
        }
        values.update(data)
        return self.url_open(url, data=values)

    def test_01_sold_out_page_shows_waitlist_button(self):
        html = self.url_open(f"/event/{self.event.id}/register").text
        self.assertIn("o_wevent_waitlist_join", html)
        self.event.waitlist_enabled = False
        html = self.url_open(f"/event/{self.event.id}/register").text
        self.assertNotIn("o_wevent_waitlist_join", html)

    def test_02_not_sold_out_no_button(self):
        self.reg_1.write({"state": "cancel"})
        html = self.url_open(f"/event/{self.event.id}/register").text
        self.assertNotIn("o_wevent_waitlist_join", html)

    def test_03_join_from_website(self):
        res = self._join(phone="+49 221 1")
        self.assertEqual(res.status_code, 200)
        self.assertIn("You are on the waiting list", res.text)
        entry = self.env["event.waitlist"].search([("event_id", "=", self.event.id)])
        self.assertEqual(len(entry), 1)
        self.assertEqual(
            (entry.name, entry.phone, entry.state),
            ("Web Visitor", "+49 221 1", "waiting"),
        )
        # Same email again: refused with a clear message
        res = self._join(email="WEB.visitor@example.com")
        self.assertIn("already on the waiting list", res.text)
        self.assertEqual(
            self.env["event.waitlist"].search_count([("event_id", "=", self.event.id)]),
            1,
        )

    def test_04_validation_and_honeypot(self):
        res = self._join(email="not-an-email")
        self.assertIn("valid email", res.text)
        res = self._join(seats="50")
        self.assertIn("between 1 and", res.text)
        self._join(website_url_hp="http://spam.example.com")
        self.assertFalse(
            self.env["event.waitlist"].search([("event_id", "=", self.event.id)])
        )

    def test_05_refused_when_not_sold_out_or_full(self):
        self.reg_1.write({"state": "cancel"})
        res = self._join()
        self.assertIn("not open", res.text)
        self.assertFalse(
            self.env["event.waitlist"].search([("event_id", "=", self.event.id)])
        )

    def test_10_token_page_and_accept(self):
        entry = self._add_entry("Alice")
        self.reg_1.write({"state": "cancel"})
        self.assertEqual(entry.state, "offered")
        url = f"/event/waitlist/{entry.access_token}"
        # GET never changes anything (mail scanners)
        html = self.url_open(url + "?action=accept").text
        self.assertIn("Yes, I take the seat", html)
        self.assertEqual(entry.state, "offered")
        res = self.url_open(url + "/accept", data={"csrf_token": self._csrf(url)})
        self.assertEqual(res.status_code, 200)
        entry.invalidate_recordset()
        self.assertEqual(entry.state, "confirmed")
        self.assertIn("your seat is confirmed", res.text)

    def test_11_token_leave_and_decline(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        url = f"/event/waitlist/{bob.access_token}"
        self.url_open(url + "/leave", data={"csrf_token": self._csrf(url)})
        bob.invalidate_recordset()
        self.assertEqual(bob.state, "cancelled")
        self.reg_1.write({"state": "cancel"})
        url = f"/event/waitlist/{alice.access_token}"
        self.url_open(url + "/decline", data={"csrf_token": self._csrf(url)})
        alice.invalidate_recordset()
        self.assertEqual(alice.state, "declined")

    def test_12_bad_tokens(self):
        self.assertEqual(self.url_open("/event/waitlist/short").status_code, 404)
        self.assertEqual(self.url_open("/event/waitlist/" + "x" * 43).status_code, 404)
        entry = self._add_entry("Alice")
        res = self.url_open(f"/event/waitlist/{entry.access_token}/accept")
        self.assertNotEqual(res.status_code, 200)  # GET not allowed

    def test_13_expired_offer_on_page(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        self.reg_1.write({"state": "cancel"})
        alice.offer_deadline = fields.Datetime.now() - timedelta(minutes=1)
        html = self.url_open(f"/event/waitlist/{alice.access_token}").text
        self.assertIn("was not confirmed in time", html)
        bob.invalidate_recordset()
        self.assertEqual(bob.state, "offered")

    def test_06_form_page(self):
        url = f"/event/{self.event.id}/waitlist"
        html = self.url_open(url + "?ticket_id=1").text
        self.assertIn('name="email"', html)
        # Logged-in visitors get their data prefilled and linked
        self.authenticate("wl_event_user", "wl_event_user")
        html = self.url_open(url).text
        self.assertIn("event.user@example.com", html)
        self._join(name="Event User", email="event.user@example.com")
        entry = self.env["event.waitlist"].search([("event_id", "=", self.event.id)])
        self.assertEqual(entry.partner_id, self.event_user.partner_id)
        # Switched off: no form at all
        self.event.waitlist_enabled = False
        self.assertEqual(self.url_open(url).status_code, 404)
        self.assertEqual(self._join().status_code, 404)

    def test_07_more_validation(self):
        res = self._join(name=" ")
        self.assertIn("enter your name and email", res.text)
        res = self._join(seats="many")
        self.assertIn("between 1 and", res.text)
        self.event.waitlist_max_size = 1
        self._add_entry("Alice")
        res = self._join()
        self.assertIn("waiting list is full", res.text)

    def test_08_tickets(self):
        event = self.env["event.event"].create(
            {
                "name": "Ticket course",
                "date_begin": self.now + timedelta(days=3),
                "date_end": self.now + timedelta(days=3, hours=1),
                "waitlist_enabled": True,
                "website_published": True,
                "event_mail_ids": [(5, 0, 0)],
                "event_ticket_ids": [
                    (5, 0, 0),
                    (0, 0, {"name": "Members", "seats_max": 1}),
                    (0, 0, {"name": "Guests", "seats_max": 1}),
                ],
            }
        )
        members, guests = event.event_ticket_ids
        self.env["event.registration"].create(
            [
                {"event_id": event.id, "event_ticket_id": t.id, "name": t.name}
                for t in (members, guests)
            ]
        )
        res = self._join(event=event)
        self.assertIn("choose a ticket", res.text)
        res = self._join(event=event, ticket_id=str(guests.id))
        self.assertIn("You are on the waiting list", res.text)
        entry = self.env["event.waitlist"].search([("event_id", "=", event.id)])
        self.assertEqual(entry.event_ticket_id, guests)

    def test_09_refused_on_create(self):
        """The checks of the form can be outdated when the entry is created
        (concurrent sign-ups): the visitor gets a message, no error page."""
        self._add_entry("Visitor", email="web.visitor@example.com")
        Controller = WebsiteEventWaitlistController
        Waitlist = type(self.env["event.waitlist"])
        with (
            patch.object(Controller, "_waitlist_validate", lambda *a: False),
            mute_logger("odoo.sql_db"),
        ):
            res = self._join()
            self.assertIn("could not add you", res.text)
            with patch.object(Waitlist, "_check_duplicate_values", lambda *a: None):
                res = self._join()
            self.assertIn("already on the waiting list", res.text)
            self.event.waitlist_max_size = 1
            res = self._join(email="other@example.com")
            self.assertIn("waiting list is full", res.text)

    def test_14_token_actions_edge_cases(self):
        alice = self._add_entry("Alice")
        url = f"/event/waitlist/{alice.access_token}"
        csrf = {"csrf_token": self._csrf(url)}
        self.assertEqual(self.url_open(url + "/dance", data=csrf).status_code, 404)
        # Accepting without an offer changes nothing
        res = self.url_open(url + "/accept", data=csrf)
        self.assertEqual(res.status_code, 200)
        alice.invalidate_recordset()
        self.assertEqual(alice.state, "waiting")
        # Accepting an offer that ran out
        self.reg_1.write({"state": "cancel"})
        alice.offer_deadline = fields.Datetime.now() - timedelta(minutes=1)
        res = self.url_open(url + "/accept", data=csrf)
        self.assertIn("message=expired", res.url)
        alice.invalidate_recordset()
        self.assertEqual(alice.state, "expired")

    def test_15_token_action_error(self):
        alice = self._add_entry("Alice")
        self.reg_1.write({"state": "cancel"})
        url = f"/event/waitlist/{alice.access_token}"

        def _fail(self):
            message = "Something went wrong"
            raise UserError(message)

        Waitlist = type(self.env["event.waitlist"])
        with patch.object(Waitlist, "action_decline_offer", _fail):
            res = self.url_open(url + "/decline", data={"csrf_token": self._csrf(url)})
        self.assertIn("Something went wrong", res.text)
        alice.invalidate_recordset()
        self.assertEqual(alice.state, "offered")
