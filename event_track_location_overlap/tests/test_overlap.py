# Copyright 2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from collections import namedtuple

from odoo import _
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase

Sample = namedtuple("Sample", ("a_start", "a_duration", "b_start", "b_duration"),)


class OverlappingCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "test event",
                "date_begin": "2018-01-01",
                "date_end": "2018-01-05",
            }
        )
        cls.location = cls.env["event.track.location"].create({"name": "test location"})
        # Define some example ranges, to test correct overlap evaluation
        cls.good = (
            Sample("2018-01-01 09:00:00", 3, "2018-01-02 09:00:00", 3),
            Sample("2018-01-04 09:00:00", 3, "2018-01-03 09:00:00", 3),
        )
        cls.bad = (
            Sample("2018-01-03 09:00:00", 3, "2018-01-03 10:00:00", 3),
            Sample("2018-01-03 09:00:00", 3, "2018-01-03 08:00:00", 3),
            Sample("2018-01-03 09:00:00", 3, "2018-01-03 08:00:00", 6),
            Sample("2018-01-03 09:00:00", 3, "2018-01-03 10:00:00", 1),
        )

    def create_tracks(self, sample, raise_always):
        """Create tracks from a sample, and raise some exception."""
        with self.env.cr.savepoint():
            self.env["event.track"].create(
                {
                    "date": sample.a_start,
                    "duration": sample.a_duration,
                    "event_id": self.event.id,
                    "location_id": self.location.id,
                    "name": "test track a",
                }
            )
            self.env["event.track"].create(
                {
                    "date": sample.b_start,
                    "duration": sample.b_duration,
                    "event_id": self.event.id,
                    "location_id": self.location.id,
                    "name": "test track b",
                }
            )
            if raise_always:
                # This notifies good track creation but rolls it back
                raise Warning(_("{} worked!".format(sample)))

    def test_default(self):
        """Locations cannot overlap by default."""
        self.assertFalse(self.location.overlappable)

    def test_location_was_not_overlappable(self):
        """Create tracks in a location that wasn't overlappable."""
        for sample in self.good:
            with self.assertRaises(Warning):
                self.create_tracks(sample, True)
        for sample in self.bad:
            with self.assertRaises(ValidationError):
                self.create_tracks(sample, True)

    def test_location_was_overlappable_good(self):
        """Change location's overlappable status when it has good tracks."""
        self.location.overlappable = True
        for sample in self.good:
            self.create_tracks(sample, False)
        self.location.overlappable = False

    def test_location_was_overlappable_bad(self):
        """Change location's overlappable status when it has bad tracks."""
        self.location.overlappable = True
        for sample in self.bad:
            self.create_tracks(sample, False)
        with self.assertRaises(ValidationError):
            self.location.overlappable = False
