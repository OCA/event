# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from datetime import timedelta
from pytz import timezone
from openerp import fields
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class GeneratorCase(TransactionCase):
    def setUp(self):
        super(GeneratorCase, self).setUp()

        # Load an event
        self.event = self.env.ref("event_training.event_odoo_mixed")

        # It has 60 days of duration before starting
        self.date_begin = fields.Datetime.from_string(self.event.date_begin)
        self.tzdiff = timezone(self.event.date_tz).utcoffset(self.date_begin)
        self.event.date_end = (
            self.date_begin + timedelta(days=60) - self.tzdiff)

        # It is expected to fulfill 80 onsite hours
        self.duration_type = self.env.ref(
            "event_training_track.duration_type_onsite")
        self.duration = self.event.product_id.duration_ids.filtered(
            lambda r: r.type_id == self.duration_type)
        self.duration.duration = 80

        # Create a generator
        self.generator = self.env["event.track.generator"].create({
            "event_id": self.event.id,
            "name": u"Some trâck name",
            "start_time": 9,
            "duration": 10.25,
            "adjust_start_time": False,
            "adjust_end_time": True,
            "duration_type_id": self.duration_type.id,
            "mondays": True,
            "tuesdays": True,
            "wednesdays": True,
            "thursdays": True,
            "fridays": True,
            "saturdays": True,
            "sundays": True,
        })

    def normal_behavior(self, no_type=True):
        """Test that the normal behavior happens.

        If event lasts for 60 days, then it should have 60 10.25h tracks.

        :param bool no_type:
            Check also if tracks are generated without duration type.
        """
        self.generator.action_generate()
        self.assertEqual(len(self.event.track_ids), 60)
        self.assertEqual(
            set(self.event.mapped("track_ids.duration")),
            {10.25})
        if no_type:
            self.assertEqual(
                len(self.event.mapped("track_ids.duration_type_id")),
                0)

    def test_durations_domain(self):
        """Durations get the right domain."""
        result = self.generator._onchange_event_change_durations_domain()
        expected_durations = (self.env
                              .ref("event_training.training_type_mixed")
                              .expected_duration_type_ids)
        self.assertEqual(
            [("id", "in", expected_durations.ids)],
            result["domain"]["duration_type_id"])

    def test_stop_when_reaching_expected_durations(self):
        """Only generates enough tracks to get to reach expected duration.

        It expects 80 hours, and tracks are generated with 10.25 hours each; so
        it must generate 7 tracks of 10.25 hours and one of 8.25.
        """
        self.generator.action_generate()
        self.assertEqual(len(self.event.track_ids), 8)
        self.assertEqual(
            self.event.mapped("track_ids.duration_type_id"),
            self.generator.duration_type_id)
        for track in self.event.track_ids[:-1]:
            self.assertEqual(track.duration, 10.25)
        self.assertEqual(self.event.track_ids[-1].duration, 8.25)

    def test_no_stop_when_reaching_expected_durations(self):
        """Generates tracks until reaching event end date."""
        self.generator.stop_when_reaching_expected_durations = False
        self.normal_behavior(False)
        self.assertEqual(
            self.event.mapped("track_ids.duration_type_id"),
            self.generator.duration_type_id)

    def test_expected_hours_zero(self):
        """Error raised when zero hours are expected."""
        self.duration.duration = 0
        with self.assertRaises(ValidationError):
            self.generator.action_generate()

    def test_expected_hours_not_found(self):
        """Error raised when not found hours are expected."""
        self.duration.unlink()
        with self.assertRaises(ValidationError):
            self.generator.action_generate()

    def test_skip_no_training(self):
        """Normal behavior in non-training events."""
        self.event.product_id = self.event.type = False
        self.normal_behavior()

    def test_skip_no_duration_type(self):
        """Normal behavior when no duration is given."""
        self.generator.duration_type_id = False
        self.normal_behavior()
