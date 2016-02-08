# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from datetime import datetime
from openerp.tests.common import TransactionCase
from .. import exceptions as e


class TestSeatsPerRegistrationLimits(TransactionCase):
    """Test the minimum limits."""

    def setUp(self):
        """Create a dummy event to work with."""

        super(TestSeatsPerRegistrationLimits, self).setUp()

        self._event = self.env["event.event"].create(
            {"name": "Test",
             "date_begin": datetime.now(),
             "date_end": datetime.now()})

        # Used when creating event.registration records
        self._registrations = self.env["event.registration"].with_context(
            active_id=self._event.id,
            default_event_id=self._event.id)

    def test_less_than_one_participant(self):
        with self.assertRaises(e.NeedAtLeastOneParticipant):
            self._event.registration_seats_min = 0

    def test_max_smaller_than_min(self):
        with self.assertRaises(e.MaxSmallerThanMin):
            self._event.registration_seats_min = 10
            self._event.registration_seats_max = 9

    def test_max_per_register_bigger_than_max_per_event(self):
        with self.assertRaises(e.MaxPerRegisterBiggerThanMaxPerEvent):
            self._event.seats_max = 10
            self._event.registration_seats_max = 11

    def test_previous_registrations_fail_min(self):
        with self.assertRaises(e.PreviousRegistrationsFail):
            self._registrations.create({"nb_register": 10})
            self._event.registration_seats_min = 11

    def test_previous_registrations_fail_max(self):
        with self.assertRaises(e.PreviousRegistrationsFail):
            self._registrations.create({"nb_register": 10})
            self._event.registration_seats_max = 9

    def test_too_few_participants(self):
        with self.assertRaises(e.TooFewParticipants):
            self._event.registration_seats_min = 10
            self._registrations.create({"nb_register": 9})

    def test_too_many_participants(self):
        with self.assertRaises(e.TooManyParticipants):
            self._event.registration_seats_max = 10
            self._registrations.create({"nb_register": 11})

    def test_default_seats(self):
        self._event.registration_seats_min = 10
        registration = self._registrations.create({})
        self.assertEqual(10, registration.nb_register, "Bad default value")
