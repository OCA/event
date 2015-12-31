# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class AttendanceMonitoringCase(TransactionCase):
    """Test attendance monitoring."""
    def setUp(self):
        super(AttendanceMonitoringCase, self).setUp()
        self.event = self.env.ref("event_training.event_odoo_mixed")
        self.event2 = self.env.ref("event_training.event_odoo_online")
        self.registration = self.env.ref("event_training.student_laith_jubair")
        self.track = self.env["event.track"].create({
            "name": "Track",
            "event_id": self.event.id,
            "duration_type_id":
                self.env.ref("event_training_track.duration_type_onsite").id,
        })

    def test_attending_other_event_track(self):
        """Nobody can attend a different event."""
        self.registration.event_id = self.event2
        with self.assertRaises(ValidationError):
            self.registration.attended_track_ids |= self.track

    def test_attendees_from_other_event(self):
        """Cannot set attendees from a different event."""
        self.track.event_id = self.event2
        with self.assertRaises(ValidationError):
            self.track.registration_ids |= self.registration

    def test_change_registration_event(self):
        """Cannot change event from registration if it attended tracks."""
        self.registration.attended_track_ids |= self.track
        with self.assertRaises(ValidationError):
            self.registration.event_id = self.event2

    def test_change_track_event(self):
        """Cannot change event from track if it has attendees."""
        self.track.registration_ids |= self.registration
        with self.assertRaises(ValidationError):
            self.track.event_id = self.event2
