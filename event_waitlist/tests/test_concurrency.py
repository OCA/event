# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from datetime import timedelta

import psycopg2

from odoo import SUPERUSER_ID, api, fields
from odoo.modules.registry import Registry
from odoo.tests import BaseCase, get_db_name, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestEventWaitlistConcurrency(BaseCase):
    """Two cancellations committed at the same time must not offer the same
    person twice, nor give away more seats than are free. Uses real
    committed transactions."""

    def setUp(self):
        super().setUp()
        self.registry = Registry(get_db_name())
        with self.registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            now = fields.Datetime.now()
            event = env["event.event"].create(
                {
                    "name": "Concurrency course",
                    "date_begin": now + timedelta(days=2),
                    "date_end": now + timedelta(days=2, hours=1),
                    "seats_limited": True,
                    "seats_max": 2,
                    "waitlist_enabled": True,
                    "event_ticket_ids": [(5, 0, 0)],
                    "event_mail_ids": [(5, 0, 0)],
                }
            )
            regs = env["event.registration"].create(
                [
                    {
                        "event_id": event.id,
                        "name": f"R{i}",
                        "email": f"r{i}@example.com",
                    }
                    for i in range(2)
                ]
            )
            entries = (
                env["event.waitlist"]
                .with_context(event_waitlist_no_mail=True)
                .create(
                    [
                        {"event_id": event.id, "name": n, "email": f"{n}@example.com"}
                        for n in ("anna", "ben", "cleo")
                    ]
                )
            )
            self.event_id = event.id
            self.reg_ids = regs.ids
            self.entry_ids = entries.ids

    def tearDown(self):
        with self.registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            event = env["event.event"].browse(self.event_id)
            event.waitlist_ids.unlink()
            event.registration_ids.unlink()
            event.unlink()
        super().tearDown()

    def _env(self, cr):
        return api.Environment(cr, SUPERUSER_ID, {"event_waitlist_no_mail": True})

    def test_parallel_cancellations(self):
        """Two cancellations in concurrent transactions: the second one sees
        an outdated snapshot, must fail with a serialization error (and be
        retried, as Odoo does for every request), and then gives the next
        free seat to the next person. Transactions are interleaved in one
        thread, which makes the test deterministic."""
        reg_1, reg_2 = self.reg_ids
        with self.registry.cursor() as cr1, self.registry.cursor() as cr2:
            # Transaction 2 takes its snapshot before transaction 1 commits.
            self._env(cr2)["event.registration"].browse(reg_2).state  # noqa: B018
            self._env(cr1)["event.registration"].browse(reg_1).write(
                {"state": "cancel"}
            )
            self._env(cr1).flush_all()
            cr1.commit()  # pylint: disable=invalid-commit
            with (
                mute_logger("odoo.sql_db"),
                self.assertRaises(psycopg2.errors.SerializationFailure),
            ):
                env2 = self._env(cr2)
                env2["event.registration"].browse(reg_2).write({"state": "cancel"})
                env2.flush_all()
            cr2.rollback()
            # Retry with a fresh snapshot, like Odoo's request retry
            env2 = self._env(cr2)
            env2["event.registration"].browse(reg_2).write({"state": "cancel"})
            env2.flush_all()
            cr2.commit()  # pylint: disable=invalid-commit
        with self.registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            entries = env["event.waitlist"].browse(self.entry_ids)
            event = env["event.event"].browse(self.event_id)
            states = dict(
                zip(entries.mapped("name"), entries.mapped("state"), strict=True)
            )
            self.assertEqual(
                states, {"anna": "offered", "ben": "offered", "cleo": "waiting"}
            )
            self.assertEqual(event.waitlist_seats_held, 2)
            self.assertEqual(event.seats_available, 0)
