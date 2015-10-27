# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp.addons.training.tests.base import BaseCase
from .. import exceptions as ex


class AttendanceMonitoringCase(BaseCase):
    """Test attendance monitoring."""
    def setUp(self):
        super(AttendanceMonitoringCase, self).setUp()
        self.event.training_action_id = self.action
        self.event2 = self.event.copy()
        self.registration = self.create(
            "event.registration",
            {"name": self.student_1.name,
             "partner_id": self.student_1.id,
             "event_id": self.event.id})
        self.track = self.create(
            "event.track",
            {"name": "Track",
             "event_id": self.event.id,
             "duration_type_id": self.duration_types_good[0].id})

    def test_default_attendance_monitoring(self):
        """Track gets attendance monitoring if duration type enables it."""
        dt = self.duration_types_good[0]
        self.track._onchange_monitor_attendance()
        self.assertIs(self.track.monitor_attendance, dt.monitor_attendance)

        # Inverse it and create other track
        dt.monitor_attendance = not dt.monitor_attendance
        other_track = self.create(
            "event.track",
            {"name": "Track",
             "event_id": self.event.id,
             "duration_type_id": self.duration_types_good[0].id})
        other_track._onchange_monitor_attendance()
        self.assertIs(other_track.monitor_attendance, dt.monitor_attendance)

    def test_attending_other_event_track(self):
        """Nobody can attend a different event."""
        self.registration.event_id = self.event2
        with self.assertRaises(ex.DifferentEventError):
            self.registration.attended_track_ids |= self.track

    def test_attendees_from_other_event(self):
        """Cannot set attendees from a different event."""
        self.track.event_id = self.event2
        with self.assertRaises(ex.DifferentEventError):
            self.track.attendee_ids |= self.registration

    def test_change_registration_event(self):
        """Cannot change event from registration if it attended tracks."""
        self.registration.attended_track_ids |= self.track
        with self.assertRaises(ex.DifferentEventError):
            self.registration.event_id = self.event2

    def test_change_track_event(self):
        """Cannot change event from track if it has attendees."""
        self.track.attendee_ids |= self.registration
        with self.assertRaises(ex.DifferentEventError):
            self.track.event_id = self.event2
