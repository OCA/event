# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from datetime import timedelta
from unittest.mock import patch

from psycopg2 import IntegrityError

from odoo import fields
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger

from .common import WaitlistCommon


@tagged("post_install", "-at_install")
class TestEventWaitlist(WaitlistCommon, TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_waitlist_data(cls.env)

    def _mails(self, entry, template_xmlid):
        template = self.env.ref(template_xmlid)
        return self.env["mail.mail"].search(
            [
                ("model", "=", "event.waitlist"),
                ("res_id", "=", entry.id),
                (
                    "subject",
                    "=",
                    template._render_field("subject", entry.ids)[entry.id],
                ),
            ]
        )

    # ------------------------------------------------------------------
    # Joining
    # ------------------------------------------------------------------

    def test_01_join_sends_confirmation_with_position(self):
        self.assertTrue(self.event.event_registrations_sold_out)
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        self.assertEqual((alice.state, bob.state), ("waiting", "waiting"))
        self.assertEqual((alice.position, bob.position), (1, 2))
        self.assertEqual(self.event.waitlist_count, 2)
        mail = self._mails(bob, "event_waitlist.mail_template_waitlist_joined")
        self.assertEqual(len(mail), 1)
        self.assertIn("<strong>2</strong>", mail.body_html)
        self.assertIn(bob.access_token, mail.body_html)
        self.assertGreaterEqual(len(bob.access_token), 40)

    def test_02_duplicate_email_refused(self):
        self._add_entry("Alice", email="alice@example.com")
        with self.assertRaises(ValidationError):
            self._add_entry("Alice again", email=" ALICE@example.com ")

    def test_03_duplicate_db_guarantee(self):
        alice = self._add_entry("Alice", email="alice@example.com")
        # Bypass the python constraint: the unique index must still refuse it.
        with (
            patch.object(
                type(self.env["event.waitlist"]),
                "_check_duplicate_values",
                lambda *a, **k: None,
            ),
            mute_logger("odoo.sql_db"),
            self.assertRaises(IntegrityError),
            self.env.cr.savepoint(),
        ):
            self._add_entry("Alice twin", email="alice@example.com")
            self.env.flush_all()
        # Once she has left, she may join again
        alice.action_leave()
        self._add_entry("Alice back", email="alice@example.com")

    def test_04_max_size(self):
        self.event.waitlist_max_size = 1
        self._add_entry("Alice")
        self.assertTrue(self.event.waitlist_is_full)
        self.assertFalse(self.event._waitlist_can_join())
        with self.assertRaises(ValidationError):
            self._add_entry("Bob")

    # ------------------------------------------------------------------
    # Offer mode
    # ------------------------------------------------------------------

    def test_10_offer_on_cancellation_and_seat_is_held(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        self.reg_1.write({"state": "cancel"})
        self.assertEqual(alice.state, "offered")
        self.assertEqual(bob.state, "waiting")
        self.assertEqual(bob.position, 1)
        self.assertAlmostEqual(
            alice.offer_deadline,
            alice.offer_date + timedelta(hours=12),
            delta=timedelta(seconds=5),
        )
        # The freed seat is reserved for Alice: nobody else can take it
        self.assertEqual(self.event.seats_available, 0)
        self.assertEqual(self.event.waitlist_seats_held, 1)
        self.assertTrue(self.event.event_registrations_sold_out)
        with self.assertRaises(ValidationError):
            self.env["event.registration"].create(
                {
                    "event_id": self.event.id,
                    "name": "Intruder",
                    "email": "x@example.com",
                }
            )
        self.assertEqual(
            len(self._mails(alice, "event_waitlist.mail_template_waitlist_offer")), 1
        )
        self.assertIn("Alice", self.event.message_ids[0].body)

    def test_11_accept_offer_registers(self):
        alice = self._add_entry("Alice", seats=1, phone="+49 221 123")
        self.reg_1.write({"state": "cancel"})
        self.assertTrue(alice.action_accept_offer())
        self.assertEqual(alice.state, "confirmed")
        self.assertEqual(len(alice.registration_ids), 1)
        reg = alice.registration_ids
        self.assertEqual(
            (reg.name, reg.email, reg.state), ("Alice", alice.email, "open")
        )
        self.assertEqual(self.event.seats_available, 0)
        self.assertEqual(self.event.waitlist_seats_held, 0)
        # Event has no confirmation scheduler: the waitlist one is sent
        self.assertEqual(
            len(self._mails(alice, "event_waitlist.mail_template_waitlist_confirmed")),
            1,
        )

    def test_12_no_double_confirmation_mail(self):
        self.event.event_mail_ids = [
            (
                0,
                0,
                {
                    "interval_unit": "now",
                    "interval_type": "after_sub",
                    "template_ref": "mail.template,"
                    f"{self.env.ref('event.event_subscription').id}",
                },
            )
        ]
        alice = self._add_entry("Alice")
        self.reg_1.write({"state": "cancel"})
        alice.action_accept_offer()
        self.assertFalse(
            self._mails(alice, "event_waitlist.mail_template_waitlist_confirmed")
        )

    def test_13_decline_goes_to_next(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        self.reg_1.write({"state": "cancel"})
        alice.action_decline_offer()
        self.assertEqual(alice.state, "declined")
        self.assertEqual(bob.state, "offered")

    def test_14_expiry_by_cron_goes_to_next(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        self.reg_1.write({"state": "cancel"})
        alice.offer_deadline = fields.Datetime.now() - timedelta(minutes=1)
        self.env["event.waitlist"]._cron_process_waitlists()
        self.assertEqual(alice.state, "expired")
        self.assertEqual(bob.state, "offered")
        self.assertEqual(
            len(self._mails(alice, "event_waitlist.mail_template_waitlist_expired")), 1
        )
        # Accepting an expired offer is not possible
        self.assertFalse(alice.action_accept_offer())
        self.assertEqual(alice.state, "expired")

    def test_15_accept_after_deadline_before_cron(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        self.reg_1.write({"state": "cancel"})
        alice.offer_deadline = fields.Datetime.now() - timedelta(minutes=1)
        self.assertFalse(alice.action_accept_offer())
        self.assertEqual(alice.state, "expired")
        self.assertEqual(bob.state, "offered")

    def test_16_leave_while_offered_goes_to_next(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        self.reg_1.write({"state": "cancel"})
        alice.action_leave()
        self.assertEqual(alice.state, "cancelled")
        self.assertEqual(bob.state, "offered")

    def test_17_bigger_request_keeps_position(self):
        family = self._add_entry("Family", seats=2)
        alice = self._add_entry("Alice")
        self.reg_1.write({"state": "cancel"})
        # Only one seat: the family keeps its position, Alice gets the seat
        self.assertEqual(family.state, "waiting")
        self.assertEqual(alice.state, "offered")
        self.assertEqual(family.position, 1)
        alice.action_accept_offer()
        self.reg_2.write({"state": "cancel"})
        self.assertEqual(family.state, "waiting")
        self.event.seats_max = 4
        self.assertEqual(family.state, "offered")

    def test_18_triggers_unlink_archive_capacity(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        carol = self._add_entry("Carol")
        self.reg_1.unlink()
        self.assertEqual(alice.state, "offered")
        self.reg_2.action_archive()
        self.assertEqual(bob.state, "offered")
        self.event.seats_max = 5
        self.assertEqual(carol.state, "offered")

    def test_19_offer_deadline_capped_by_start(self):
        self.event.date_begin = fields.Datetime.now() + timedelta(hours=3)
        alice = self._add_entry("Alice")
        self.reg_1.write({"state": "cancel"})
        self.assertLessEqual(alice.offer_deadline, self.event.date_begin)

    def test_20_no_offer_after_start(self):
        alice = self._add_entry("Alice")
        self.event.write(
            {
                "date_begin": fields.Datetime.now() - timedelta(minutes=5),
                "date_end": fields.Datetime.now() + timedelta(hours=1),
            }
        )
        self.reg_1.write({"state": "cancel"})
        self.assertEqual(alice.state, "waiting")
        self.assertFalse(self.event._waitlist_can_join())

    def test_21_no_offer_when_disabled(self):
        alice = self._add_entry("Alice")
        self.event.waitlist_enabled = False
        self.reg_1.write({"state": "cancel"})
        self.assertEqual(alice.state, "waiting")
        self.event.waitlist_enabled = True
        self.assertEqual(alice.state, "offered")

    def test_22_manual_move_up_and_reset(self):
        alice = self._add_entry("Alice")
        bob = self._add_entry("Bob")
        with self.assertRaises(UserError):
            bob.action_offer_now()
        self.event.seats_max = 3
        self.assertEqual(alice.state, "offered")
        alice.action_decline_offer()
        self.assertEqual(bob.state, "offered")
        alice.action_reset_to_waiting()
        self.assertEqual(alice.state, "waiting")
        self.assertEqual(alice.position, 1)

    # ------------------------------------------------------------------
    # Automatic registration
    # ------------------------------------------------------------------

    def test_30_auto_mode_registers(self):
        self.event.waitlist_mode = "auto"
        alice = self._add_entry("Alice", seats=2)
        self.reg_1.write({"state": "cancel"})
        self.assertEqual(alice.state, "waiting")
        self.reg_2.write({"state": "cancel"})
        self.assertEqual(alice.state, "confirmed")
        self.assertEqual(
            len(alice.registration_ids.filtered(lambda r: r.state == "open")), 2
        )
        self.assertEqual(self.event.seats_available, 0)

    # ------------------------------------------------------------------
    # Tickets
    # ------------------------------------------------------------------

    def test_40_ticket_level(self):
        event = self.env["event.event"].create(
            {
                "name": "Ticket course",
                "date_begin": self.now + timedelta(days=3),
                "date_end": self.now + timedelta(days=3, hours=1),
                "waitlist_enabled": True,
                "event_mail_ids": [(5, 0, 0)],
                "event_ticket_ids": [
                    (5, 0, 0),
                    (0, 0, {"name": "Members", "seats_max": 1}),
                    (0, 0, {"name": "Guests", "seats_max": 5}),
                ],
            }
        )
        members, guests = event.event_ticket_ids
        reg = self.env["event.registration"].create(
            {"event_id": event.id, "event_ticket_id": members.id, "name": "M1"}
        )
        self.assertTrue(members.is_sold_out)
        self.assertFalse(event.event_registrations_sold_out)
        self.assertEqual(event._waitlist_joinable_tickets(), members)
        self.assertTrue(event._waitlist_can_join(members))
        self.assertFalse(event._waitlist_can_join(guests))
        alice = self._add_entry("Alice", event=event, event_ticket_id=members.id)
        self.assertEqual(alice.state, "waiting")
        reg.write({"state": "cancel"})
        self.assertEqual(alice.state, "offered")
        self.assertEqual(members.seats_available, 0)
        self.assertEqual(members.waitlist_seats_held, 1)
        alice.action_accept_offer()
        self.assertEqual(alice.registration_ids.event_ticket_id, members)

    # ------------------------------------------------------------------
    # Security, privacy
    # ------------------------------------------------------------------

    def test_50_access_rights(self):
        alice = self._add_entry("Alice")
        as_user = alice.with_user(self.event_user)
        as_user.read(["name", "state", "access_token"])
        as_user.write({"sequence": 99})
        self.env["event.waitlist"].with_user(self.event_user).create(
            {"event_id": self.event.id, "name": "Zoe", "email": "zoe@example.com"}
        )
        public = self.env.ref("base.public_user")
        portal = self.env["res.users"].create(
            {
                "name": "Portal",
                "login": "wl_portal",
                "groups_id": [(6, 0, [self.env.ref("base.group_portal").id])],
            }
        )
        for user in (public, portal):
            with self.assertRaises(AccessError):
                alice.with_user(user).read(["name"])
            with self.assertRaises(AccessError):
                self.env["event.waitlist"].with_user(user).create(
                    {"event_id": self.event.id, "name": "X", "email": "x@example.com"}
                )

    def test_51_cleanup_after_event(self):
        alice = self._add_entry("Alice")
        self.event.write(
            {
                "date_begin": fields.Datetime.now() - timedelta(days=3),
                "date_end": fields.Datetime.now() - timedelta(days=2),
                "waitlist_retention_days": 7,
            }
        )
        self.env["event.waitlist"]._cron_cleanup_waitlists()
        self.assertTrue(alice.exists())
        self.event.waitlist_retention_days = 1
        self.env["event.waitlist"]._cron_cleanup_waitlists()
        self.assertFalse(alice.exists())

    # ------------------------------------------------------------------
    # Backend actions, edge cases
    # ------------------------------------------------------------------

    def _free_seat_silently(self, registration):
        """Free a seat without moving the list up (as if not processed yet)."""
        registration.with_context(event_waitlist_no_process=True).write(
            {"state": "cancel"}
        )

    def test_60_offer_now(self):
        alice = self._add_entry("Alice")
        self._free_seat_silently(self.reg_1)
        self.assertEqual(alice.state, "waiting")
        alice.action_offer_now()
        self.assertEqual(alice.state, "offered")
        # Automatic mode registers right away
        self.event.waitlist_mode = "auto"
        bob = self._add_entry("Bob")
        self._free_seat_silently(self.reg_2)
        bob.action_offer_now()
        self.assertEqual(bob.state, "confirmed")
        self.assertEqual(bob.registration_count, 1)

    def test_61_offer_now_refused_after_start(self):
        alice = self._add_entry("Alice")
        self._free_seat_silently(self.reg_1)
        self.event.with_context(event_waitlist_no_process=True).write(
            {
                "date_begin": self.now - timedelta(hours=1),
                "date_end": self.now + timedelta(hours=1),
            }
        )
        self.assertFalse(self.event._waitlist_can_offer())
        with self.assertRaises(UserError):
            alice.action_offer_now()
        self.assertEqual(alice.state, "waiting")

    def test_62_backend_buttons(self):
        alice = self._add_entry("Alice")
        self._free_seat_silently(self.reg_1)
        self.event.action_waitlist_process()
        self.assertEqual(alice.state, "offered")
        action = self.event.action_view_waitlist()
        self.assertEqual(action["domain"], [("event_id", "=", self.event.id)])
        self.assertEqual(action["context"]["default_event_id"], self.event.id)
        alice.action_accept_offer()
        action = alice.action_view_registrations()
        self.assertEqual(
            self.env["event.registration"].search(action["domain"]),
            alice.registration_ids,
        )
        # New entries created from the list view are appended at the end
        carol = (
            self.env["event.waitlist"]
            .with_context(default_event_id=self.event.id)
            .create({"name": "Carol", "email": "carol@example.com"})
        )
        self.assertEqual(carol.sequence, alice.sequence + 1)

    def test_63_values_checked(self):
        for vals in (
            {"waitlist_offer_hours": 0},
            {"waitlist_max_size": -1},
            {"waitlist_retention_days": -1},
        ):
            with self.assertRaises(ValidationError), self.env.cr.savepoint():
                self.event.write(vals)
        other = self.env["event.event"].create(
            {
                "name": "Other",
                "date_begin": self.now + timedelta(days=1),
                "date_end": self.now + timedelta(days=2),
                "event_ticket_ids": [(5, 0, 0), (0, 0, {"name": "Other ticket"})],
            }
        )
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            self._add_entry("Alice", event_ticket_id=other.event_ticket_ids.id)
        alice = self._add_entry("Alice")
        alice.write({"email": " Alice.New@Example.com"})
        self.assertEqual(alice.email_normalized, "alice.new@example.com")

    def test_64_registration_changes(self):
        alice = self._add_entry("Alice")
        # Writes that do not free a seat change nothing
        self.reg_1.write({"name": "Renamed"})
        self.assertEqual(alice.state, "waiting")
        other = self.env["event.event"].create(
            {
                "name": "Other",
                "date_begin": self.now + timedelta(days=1),
                "date_end": self.now + timedelta(days=2),
            }
        )
        # Moving an attendee to another event frees the seat
        self.reg_1.write({"event_id": other.id})
        self.assertEqual(alice.state, "offered")
        # Seats held for an offer can be ignored (used by sale bridges)
        event = self.event.with_context(event_waitlist_ignore_entry_ids=alice.ids)
        self.assertEqual(event.waitlist_seats_held, 0)
        self.assertEqual(event.seats_available, 1)

    def _ticket_event(self):
        event = self.env["event.event"].create(
            {
                "name": "Ticket course",
                "date_begin": self.now + timedelta(days=3),
                "date_end": self.now + timedelta(days=3, hours=1),
                "waitlist_enabled": True,
                "event_mail_ids": [(5, 0, 0)],
                "event_ticket_ids": [
                    (5, 0, 0),
                    (0, 0, {"name": "Members", "seats_max": 1}),
                    (0, 0, {"name": "Guests", "seats_max": 5}),
                ],
            }
        )
        members, guests = event.event_ticket_ids
        reg = self.env["event.registration"].create(
            {"event_id": event.id, "event_ticket_id": members.id, "name": "M1"}
        )
        return event, members, guests, reg

    def test_65_ticket_capacity_and_ignore(self):
        event, members, guests, reg = self._ticket_event()
        alice = self._add_entry("Alice", event=event, event_ticket_id=members.id)
        members.seats_max = 2
        self.assertEqual(alice.state, "offered")
        self.assertEqual(members.waitlist_seats_held, 1)
        members_ignoring = members.with_context(
            event_waitlist_ignore_entry_ids=alice.ids
        )
        self.assertEqual(members_ignoring.waitlist_seats_held, 0)
        self.assertEqual(members_ignoring.seats_available, 1)

    def test_66_expired_ticket_not_served(self):
        event, members, guests, reg = self._ticket_event()
        alice = self._add_entry("Alice", event=event, event_ticket_id=members.id)
        members.end_sale_datetime = self.now - timedelta(hours=1)
        reg.write({"state": "cancel"})
        # Sales of her ticket are over: no seat for Alice
        self.assertEqual(alice.state, "waiting")
        self.assertTrue(event._waitlist_can_offer())
        guests.end_sale_datetime = self.now - timedelta(hours=1)
        self.assertFalse(event._waitlist_can_offer())

    def test_67_cron_failure_on_one_event(self):
        alice = self._add_entry("Alice")
        self.reg_1.write({"state": "cancel"})
        alice.offer_deadline = fields.Datetime.now() - timedelta(minutes=1)
        Waitlist = type(self.env["event.waitlist"])

        def _fail(self):
            message = "boom"
            raise UserError(message)

        with (
            patch.object(Waitlist, "_waitlist_expire_overdue", _fail),
            mute_logger("odoo.addons.event_waitlist.models.event_waitlist"),
        ):
            self.env["event.waitlist"]._cron_process_waitlists()
        # Nothing was changed for this event, the cron did not crash
        self.assertEqual(alice.state, "offered")
        self.env["event.waitlist"]._cron_process_waitlists()
        self.assertEqual(alice.state, "expired")
