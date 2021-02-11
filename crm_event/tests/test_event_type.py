# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta
from odoo.tests.common import SavepointCase


class EventTypeCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Event type test data
        cls.type_a = cls.env["event.type"].create({"name": "Event type A"})
        cls.type_b = cls.env["event.type"].create({"name": "Event type B"})
        # Event test data
        cls.a_events = cls.env["event.event"].create(
            [
                {
                    "event_type_id": cls.type_a.id,
                    "date_begin": datetime.now() - timedelta(days=1),
                    "date_end": datetime.now() - timedelta(minutes=1),
                    "name": "Today's past event",
                    "seats_availability": "limited",
                    "seats_max": 1,
                },
                {
                    "event_type_id": cls.type_a.id,
                    "date_begin": datetime.now() - timedelta(days=2),
                    "date_end": datetime.now() - timedelta(days=1),
                    "name": "Yesterday's past event",
                    "seats_availability": "limited",
                    "seats_max": 10,
                },
                {
                    "event_type_id": cls.type_a.id,
                    "date_begin": datetime.now() - timedelta(days=1),
                    "date_end": datetime.now() + timedelta(days=1),
                    "name": "Present event",
                    "seats_availability": "limited",
                    "seats_max": 100,
                },
                {
                    "event_type_id": cls.type_a.id,
                    "date_begin": datetime.now() + timedelta(days=1),
                    "date_end": datetime.now() + timedelta(days=2),
                    "name": "Future event",
                    "seats_availability": "limited",
                    "seats_max": 1000,
                },
            ]
        )
        for event in cls.a_events:
            cls.a_events |= event.copy({"active": False})
        cls.b_events = cls.env["event.event"]
        for event in cls.a_events:
            cls.b_events |= event.copy({"event_type_id": cls.type_b.id})
        cls.b_events[0].seats_availability = "unlimited"
        # Leads and opportunities test data
        cls.opportunities = cls.env["crm.lead"].create(
            [
                {
                    "event_type_id": cls.type_a.id,
                    "name": "new",
                    "probability": 0,
                    "seats_wanted": 1,
                    "type": "opportunity",
                },
                {
                    "event_type_id": cls.type_a.id,
                    "name": "running",
                    "probability": 50,
                    "seats_wanted": 10,
                    "type": "opportunity",
                },
                {
                    "event_type_id": cls.type_a.id,
                    "name": "won",
                    "probability": 100,
                    "seats_wanted": 100,
                    "type": "opportunity",
                },
                {
                    "active": False,
                    "event_type_id": cls.type_a.id,
                    "name": "lost",
                    "probability": 0,
                    "seats_wanted": 1000,
                    "type": "opportunity",
                },
            ]
        )
        cls.leads = cls.env["crm.lead"]
        for opp in cls.opportunities:
            cls.leads |= opp.copy({"type": "lead"})

    def test_event_totals(self):
        self.assertEqual(self.type_a.seats_available_total, "3 (1101)")
        self.assertEqual(self.type_b.seats_available_total, "3 (Unlimited)")

    def test_opportunity_totals(self):
        self.assertEqual(self.type_a.seats_wanted_total, "2 (11)")
        self.assertEqual(self.type_b.seats_wanted_total, "0 (0)")
