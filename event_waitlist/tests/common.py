# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from datetime import timedelta

from odoo import fields

from odoo.addons.mail.tests.common import mail_new_test_user


class WaitlistCommon:
    @classmethod
    def _setup_waitlist_data(cls, env):
        cls.env = env
        cls.now = fields.Datetime.now()
        cls.event_user = mail_new_test_user(
            env,
            login="wl_event_user",
            groups="base.group_user,event.group_event_user",
            name="Event User",
            email="event.user@example.com",
        )
        cls.event = env["event.event"].create(
            {
                "name": "Waitlist Test Course",
                "date_begin": cls.now + timedelta(days=5),
                "date_end": cls.now + timedelta(days=5, hours=2),
                "seats_limited": True,
                "seats_max": 2,
                "waitlist_enabled": True,
                "waitlist_mode": "offer",
                "waitlist_offer_hours": 12,
                "event_ticket_ids": [(5, 0, 0)],
                "event_mail_ids": [(5, 0, 0)],
            }
        )
        cls.reg_1, cls.reg_2 = env["event.registration"].create(
            [
                {
                    "event_id": cls.event.id,
                    "name": "Attendee 1",
                    "email": "a1@example.com",
                },
                {
                    "event_id": cls.event.id,
                    "name": "Attendee 2",
                    "email": "a2@example.com",
                },
            ]
        )

    @classmethod
    def _add_entry(cls, name, seats=1, event=None, **vals):
        values = {
            "event_id": (event or cls.event).id,
            "name": name,
            "email": f"{name.lower().replace(' ', '.')}@example.com",
            "seats": seats,
        }
        values.update(vals)
        return cls.env["event.waitlist"].create(values)
