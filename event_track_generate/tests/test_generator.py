# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from datetime import datetime
from itertools import product
from pytz import timezone
from openerp import fields
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class GeneratorCase(TransactionCase):
    def setUp(self):
        super(GeneratorCase, self).setUp()

        # Create an event
        begin = datetime(2015, 8, 10, 7)
        self.event = self.env["event.event"].create({
            "name": "Test event %s" % __name__,
            "date_begin": begin,  # Monday
            "date_end": datetime(2015, 8, 23, 22),  # Sunday
            "date_tz": "Europe/Madrid"})
        self.tzdiff = timezone(self.event.date_tz).utcoffset(begin)

        # Add some tracks to the event
        for day in range(10, 14):
            self.event.track_ids |= self.env["event.track"].create({
                "name": u"Traçk name",
                "event_id": self.event.id,
                "date": datetime(2015, 8, day, 10, 15) - self.tzdiff,
                "duration": 2.75})

        # Create a generator
        self.generator = self.env["event.track.generator"].create({
            "event_id": self.event.id,
            "name": u"Some trâck name",
            "start_time": 10.25,
            "duration": 2.75,
            "adjust_start_time": False,
            "adjust_end_time": False})

    def test_adjust_start_time(self):
        """Event start time is adjusted correctly."""
        self.generator.adjust_start_time = True
        self.generator.mondays = True
        self.generator.action_generate()
        self.assertEqual(
            fields.Datetime.from_string(self.event.date_begin),
            datetime(2015, 8, 10, 10, 15) - self.tzdiff)

    def test_adjust_end_time(self):
        """Event end time is adjusted correctly."""
        self.generator.adjust_end_time = True
        self.generator.sundays = True
        self.generator.action_generate()
        self.assertEqual(
            fields.Datetime.from_string(self.event.date_end),
            datetime(2015, 8, 23, 13) - self.tzdiff)

    def test_end_time(self):
        """Test if end time is measured right."""
        self.assertEqual(
            self.generator.end_time,
            self.generator.start_time + self.generator.duration)

    def test_with_weekdays_and_delete_existing_tracks(self):
        """Test generating all possible weekdays combination.

        Test also if the deletion of existing tracks work.
        """
        # Delete tracks each time to check if correct weekdays are created
        self.generator.delete_existing_tracks = True

        # Get all possible weekday combinations
        for days in product([True, False], repeat=7):

            # For no weekdays, there's the test :meth:`~.test_without_weekdays`
            if True in days:
                (self.generator.mondays,
                 self.generator.tuesdays,
                 self.generator.wednesdays,
                 self.generator.thursdays,
                 self.generator.fridays,
                 self.generator.saturdays,
                 self.generator.sundays) = days

                # Generate tracks
                self.generator.action_generate()

                # This will be used to know if they were generated fine
                generated_weekdays = [0] * 7

                for track in self.event.track_ids.exists():
                    start_dt = fields.Datetime.from_string(track.date)

                    # Count how many days were generated with this weekday
                    generated_weekdays[start_dt.weekday()] += 1

                # There must be 2 or 0 days of each
                self.assertEqual(
                    set(generated_weekdays),
                    {0, 2} if False in days else {2})

                # Check that only the requested weekdays were generated
                self.assertEqual(
                    tuple(bool(w) for w in generated_weekdays),
                    days)

    def test_without_deleting_existing_tracks(self):
        """Test generating tracks without deleting existing ones."""
        self.generator.delete_existing_tracks = False
        current = len(self.event.track_ids.exists())

        # Must generate 1 monday
        self.generator.mondays = True
        self.generator.action_generate()
        current += 1
        self.assertEqual(current, len(self.event.track_ids.exists()))

        # Must generate 2 sundays
        self.generator.sundays = True
        self.generator.action_generate()
        current += 2
        self.assertEqual(current, len(self.event.track_ids.exists()))

    def test_without_weekdays(self):
        """Test trying to generate tracks without setting weekdays."""
        with self.assertRaises(ValidationError):
            self.generator.action_generate()
