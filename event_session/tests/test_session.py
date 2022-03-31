# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _
from odoo.exceptions import ValidationError
from odoo.tests import common

from ..models.event_session import (
    datetime_format,
    get_locale,
    localized_format,
    time_format,
)


class EventSession(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(EventSession, cls).setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-30 22:00:00",
                "seats_limited": True,
                "seats_max": "5",
            }
        )
        cls.session = cls.env["event.session"].create(
            {
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-26 22:00:00",
                "event_id": cls.event.id,
                "seats_limited": cls.event.seats_limited,
                "seats_max": cls.event.seats_max,
            }
        )
        cls.attendee = cls.env["event.registration"].create(
            {
                "name": "Test attendee",
                "event_id": cls.event.id,
                "session_id": cls.session.id,
            }
        )
        cls.wizard = cls.env["wizard.event.session"].create(
            {
                "event_id": cls.event.id,
                "mondays": True,
                "tuesdays": True,
                "wednesdays": True,
                "thursdays": False,
                "fridays": True,
                "sundays": True,
                "saturdays": True,
                "delete_existing_sessions": False,
                "session_hour_ids": [(0, 0, {"start_time": 20.0, "end_time": 21.0})],
            }
        )
        cls.template = cls.env["event.mail.template"].create(
            {
                "name": "Template test 01",
                "scheduler_template_ids": [
                    (
                        0,
                        0,
                        {
                            "interval_nbr": 15,
                            "interval_unit": "days",
                            "interval_type": "before_event",
                            "template_id": cls.env.ref("event.event_reminder").id,
                        },
                    )
                ],
            }
        )
        cls.scheduler = cls.env["event.mail"].create(
            {
                "event_id": cls.event.id,
                "session_id": cls.session.id,
                "interval_type": "after_sub",
                "template_id": cls.template.id,
            }
        )
        cls.mail_registration = cls.env["event.mail.registration"].create(
            {"scheduler_id": cls.scheduler.id, "registration_id": cls.attendee.id}
        )

        # Enable all languages used in the tests without loading them
        languages = cls.env["res.lang"].search(
            [
                ["code", "in", ["en_US", "fr_FR", "fr_CA", "en_CA", "ru_RU"]],
                "|",
                ["active", "=", True],
                ["active", "=", False],
            ]
        )
        languages.write({"active": True})

    def test_session_name_get(self):
        self.assertEqual(
            self.session.name_get()[0][1],
            "[Test event] " + self.session.name,
        )

    def test_check_beginning_date(self):
        self.session.date_begin = "2017-05-26 20:00:00"
        with self.assertRaises(ValidationError):
            self.session.date_begin = "2017-05-26 19:59:59"
        with self.assertRaises(ValidationError):
            self.session.date_end = "2017-05-30 22:00:01"

    def test_check_end_date(self):
        self.session.date_end = "2017-05-30 22:00:00"
        with self.assertRaises(ValidationError):
            self.session.date_end = "2017-05-30 22:00:01"
        with self.assertRaises(ValidationError):
            self.session.date_end = "2017-05-26 19:59:59"

    def test_check_zero_duration(self):
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.session.write(
                {
                    "date_begin": "2017-05-28 22:00:00",
                    "date_end": "2017-05-28 22:00:00",
                }
            )

    def test_open_registrations(self):
        # registrations button
        res = self.session.button_open_registration()
        attendees = self.env["event.registration"].search(
            [["session_id", "=", self.session.id]]
        )
        self.assertEqual(res["domain"], [("id", "in", attendees.ids)])

    def test_assign_mail_template(self):
        vals = {
            "event_mail_ids": self.session._session_mails_from_template(self.event.id)
        }
        self.session.write(vals)
        self.assertEqual(len(self.session.event_mail_ids), 0)
        vals = {
            "event_mail_ids": self.session._session_mails_from_template(
                self.event.id, self.template
            )
        }
        self.session.write(vals)
        self.assertEqual(len(self.session.event_mail_ids), 1)

    def test_session_seats(self):
        """Session seat"""
        self.assertEqual(self.event.seats_available, self.session.seats_available)
        self.assertEqual(self.event.seats_unconfirmed, self.session.seats_unconfirmed)
        self.assertEqual(self.event.seats_used, self.session.seats_used)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # check limit regs
            for _i in range(int(self.session.seats_available) + 1):
                self.env["event.registration"].create(
                    {
                        "name": "Test Attendee",
                        "event_id": self.event.id,
                        "session_id": self.session.id,
                        "state": "open",
                    }
                )

    def test_compute_name(self):
        vals = {
            "date_begin": "2017-05-28 22:00:00",
            "date_end": "2017-05-28 23:00:00",
        }
        session = self.env["event.session"].new(vals)
        self.assertEqual(session.name, "Sunday 5/28/17, 10:00 PM - 11:00 PM")
        session.date_begin = session.date_end = False
        self.assertEqual(session.name, "/")

    def test_wizard(self):
        """Test Session Generation Wizard"""
        self.event.date_end = "2017-06-11 23:59:59"
        self.event.date_begin = "2017-06-05 00:00:00"
        self.wizard.delete_existing_sessions = False
        self.wizard.action_generate_sessions()
        # Delete previous sessions
        self.wizard.update({"delete_existing_sessions": True})
        self.wizard.update({"event_mail_template_id": self.template})
        with self.assertRaises(ValidationError) as error, self.cr.savepoint():
            self.wizard.action_generate_sessions()
            self.assertEqual(
                error,
                _(
                    "You are trying to delete one or more \
            sessions with active registrations"
                ),
            )
        self.attendee.session_id = False
        self.wizard.action_generate_sessions()
        sessions = self.env["event.session"].search([["event_id", "=", self.event.id]])
        self.assertEqual(len(sessions), 6)
        for session in sessions:
            self.assertTrue(session.event_mail_ids)
            self.assertEqual(session.seats_max, self.event.seats_max)
            self.assertEqual(session.seats_limited, self.event.seats_limited)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # session duration = 0
            self.wizard.update(
                {"session_hour_ids": [(0, 0, {"start_time": 20.0, "end_time": 20.0})]}
            )
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # hour invalidity
            self.wizard.update(
                {"session_hour_ids": [(0, 0, {"start_time": 24.0, "end_time": 24.1})]}
            )
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # schedules overlap
            self.wizard.update(
                {
                    "session_hour_ids": [
                        (0, 0, {"start_time": 20.0, "end_time": 21.0}),
                        (0, 0, {"start_time": 20.5, "end_time": 21.5}),
                    ],
                }
            )
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.wizard.update(
                {
                    "session_hour_ids": [
                        (0, 0, {"start_time": 20.0, "end_time": 21.0}),
                        (0, 0, {"start_time": 19.5, "end_time": 21.5}),
                    ],
                }
            )
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # weekday not set
            self.wizard.update(
                {
                    "mondays": False,
                    "tuesdays": False,
                    "wednesdays": False,
                    "thursdays": False,
                    "fridays": False,
                    "sundays": False,
                    "saturdays": False,
                }
            )
            self.wizard.action_generate_sessions()

    def test_event_mail_compute_scheduled_date(self):
        date = self.scheduler.session_id.create_date + relativedelta(hours=+1)
        self.assertEqual(self.scheduler.scheduled_date, date)
        self.scheduler.update({"interval_type": "before_event"})
        date = self.scheduler.session_id.date_begin + relativedelta(hours=-1)
        self.assertEqual(self.scheduler.scheduled_date, date)
        self.scheduler.update({"interval_type": "after_event"})
        date = self.scheduler.session_id.date_end + relativedelta(hours=+1)
        self.assertEqual(self.scheduler.scheduled_date, date)

    def test_event_mail_registration_compute_scheduled_date(self):
        self.scheduler.update({"interval_unit": "days"})
        date = self.mail_registration.registration_id.date_open + relativedelta(days=+1)
        self.assertEqual(self.mail_registration.scheduled_date, date)

    def test_get_locale(self):
        """
        Check if the locale correctly return from the locale set
        in the context of the environment.
        """
        session = self.env["event.session"]
        # Check a locale that can't be the default one
        locale = get_locale(session.with_context(lang="fr_CA").env)
        self.assertEqual(locale.language, "fr")
        self.assertEqual(locale.territory, "CA")
        # Check locale change to en_US
        locale = get_locale(session.with_context(lang="en_US").env)
        self.assertEqual(locale.language, "en")
        self.assertEqual(locale.territory, "US")
        # Check locale change to Russian
        locale = get_locale(session.with_context(lang="ru_RU").env)
        self.assertEqual(locale.language, "ru")
        self.assertEqual(locale.territory, "RU")
        # Check default locale when lang is None should be en_US
        locale = get_locale(session.with_context(lang=None).env)
        self.assertEqual(locale.language, "en")
        self.assertEqual(locale.territory, "US")

    def test_time_format(self):
        session = self.env["event.session"]
        datetime_val = datetime(2020, 1, 1, 15, 30)
        short_time = time_format("short")
        # Create some locales
        locale_us = get_locale(session.with_context(lang="en_US").env)
        locale_ru = get_locale(session.with_context(lang="ru_RU").env)
        locale_enca = get_locale(session.with_context(lang="en_CA").env)
        locale_frca = get_locale(session.with_context(lang="fr_CA").env)
        locale_frfr = get_locale(session.with_context(lang="fr_FR").env)
        # Check that result of short time is indeed the one of the locale
        # being passed explicitly as string or as Locale from get_locale
        # Check US format
        short_time_us = short_time(datetime_val, locale_us)
        short_time_us2 = short_time(datetime_val, "en_US")
        self.assertEqual(short_time_us, "3:30 PM")
        self.assertEqual(short_time_us, short_time_us2)
        # Check en_CA format
        short_time_enca = short_time(datetime_val, locale_enca)
        short_time_enca2 = short_time(datetime_val, "en_CA")
        self.assertEqual(short_time_enca, "3:30 p.m.")
        self.assertEqual(short_time_enca, short_time_enca2)
        # Check fr_CA format
        short_time_frca = short_time(datetime_val, locale_frca)
        short_time_frca2 = short_time(datetime_val, "fr_CA")
        self.assertEqual(short_time_frca, "15 h 30")
        self.assertEqual(short_time_frca, short_time_frca2)
        # Check fr_FR  format
        short_time_frfr = short_time(datetime_val, locale_frfr)
        short_time_frfr2 = short_time(datetime_val, "fr_FR")
        self.assertEqual(short_time_frfr, "15:30")
        self.assertEqual(short_time_frfr, short_time_frfr2)
        # Check ru_RU format
        short_time_ru = short_time(datetime_val, locale_ru)
        short_time_ru2 = short_time(datetime_val, "ru_RU")
        self.assertEqual(short_time_ru, "15:30")
        self.assertEqual(short_time_ru, short_time_ru2)

    def test_datetime_format(self):
        """
        Check the datetime_format method works with different locales
        """
        session = self.env["event.session"]
        datetime_val = datetime(2020, 1, 31, 15, 30)
        short_time = datetime_format("short")
        weekday_time = datetime_format("EEEE")
        # Create some locales
        locale_us = get_locale(session.with_context(lang="en_US").env)
        locale_ru = get_locale(session.with_context(lang="ru_RU").env)
        locale_enca = get_locale(session.with_context(lang="en_CA").env)
        locale_frca = get_locale(session.with_context(lang="fr_CA").env)
        locale_frfr = get_locale(session.with_context(lang="fr_FR").env)
        # Check that result of short time is indeed the one of the locale
        # being passed explicitly as string or as Locale from get_locale
        # Check US format
        short_time_us = short_time(datetime_val, locale_us)
        short_time_us2 = short_time(datetime_val, "en_US")
        self.assertEqual(short_time_us, "1/31/20, 3:30 PM")
        self.assertEqual(short_time_us, short_time_us2)
        # Check en_CA format
        short_time_enca = short_time(datetime_val, locale_enca)
        short_time_enca2 = short_time(datetime_val, "en_CA")
        self.assertEqual(short_time_enca, "2020-01-31, 3:30 p.m.")
        self.assertEqual(short_time_enca, short_time_enca2)
        # Check fr_CA format
        short_time_frca = short_time(datetime_val, locale_frca)
        short_time_frca2 = short_time(datetime_val, "fr_CA")
        self.assertEqual(short_time_frca, "20-01-31 15 h 30")
        self.assertEqual(short_time_frca, short_time_frca2)
        # Check fr_FR  format
        short_time_frfr = short_time(datetime_val, locale_frfr)
        short_time_frfr2 = short_time(datetime_val, "fr_FR")
        self.assertEqual(short_time_frfr, "31/01/2020 15:30")
        self.assertEqual(short_time_frfr, short_time_frfr2)
        # Check ru_RU format
        short_time_ru = short_time(datetime_val, locale_ru)
        short_time_ru2 = short_time(datetime_val, "ru_RU")
        self.assertEqual(short_time_ru, "31.01.2020, 15:30")
        self.assertEqual(short_time_ru, short_time_ru2)

        # Check week days formatted
        weekday_us = weekday_time(datetime_val, locale_us)
        weekday_us2 = weekday_time(datetime_val, "en_US")
        self.assertEqual(weekday_us, "Friday")
        self.assertEqual(weekday_us, weekday_us2)
        # Check en_CA format
        weekday_enca = weekday_time(datetime_val, locale_enca)
        weekday_enca2 = weekday_time(datetime_val, "en_CA")
        self.assertEqual(weekday_enca, "Friday")
        self.assertEqual(weekday_enca, weekday_enca2)
        # Check fr_CA format
        weekday_frca = weekday_time(datetime_val, locale_frca)
        weekday_frca2 = weekday_time(datetime_val, "fr_CA")
        self.assertEqual(weekday_frca, "vendredi")
        self.assertEqual(weekday_frca, weekday_frca2)
        # Check fr_FR  format
        weekday_frfr = weekday_time(datetime_val, locale_frfr)
        weekday_frfr2 = weekday_time(datetime_val, "fr_FR")
        self.assertEqual(weekday_frfr, "vendredi")
        self.assertEqual(weekday_frfr, weekday_frfr2)
        # Check ru_RU
        weekday_ru = weekday_time(datetime_val, locale_ru)
        weekday_ru2 = weekday_time(datetime_val, "ru_RU")
        self.assertEqual(weekday_ru, "пятница")
        self.assertEqual(weekday_ru, weekday_ru2)

    def test_check_localized_format(self):
        """
        Check that localized_format can format multiple
        time format in one string seperated by spaces according
        to the context language.
        """
        session = self.env["event.session"]

        datetime_val = datetime(2020, 1, 31, 15, 30)
        # Create some locales
        locale_us = get_locale(session.with_context(lang="en_US").env)
        locale_ru = get_locale(session.with_context(lang="ru_RU").env)
        locale_enca = get_locale(session.with_context(lang="en_CA").env)
        locale_frca = get_locale(session.with_context(lang="fr_CA").env)
        locale_frfr = get_locale(session.with_context(lang="fr_FR").env)

        # Create a list of formats to test which result in a string with
        # the formated text separated by a space
        # "formated1 formated2 formated3"
        formats = [
            datetime_format("EEEE"),
            datetime_format("short"),
            time_format("short"),
        ]

        self.assertEqual(
            localized_format(datetime_val, formats, locale_us),
            "Friday 1/31/20, 3:30 PM 3:30 PM",
        )
        self.assertEqual(
            localized_format(datetime_val, formats, locale_enca),
            "Friday 2020-01-31, 3:30 p.m. 3:30 p.m.",
        )
        self.assertEqual(
            localized_format(datetime_val, formats, locale_frca),
            "vendredi 20-01-31 15 h 30 15 h 30",
        )
        self.assertEqual(
            localized_format(datetime_val, formats, locale_frfr),
            "vendredi 31/01/2020 15:30 15:30",
        )
        self.assertEqual(
            localized_format(datetime_val, formats, locale_ru),
            "пятница 31.01.2020, 15:30 15:30",
        )

    def test_atendee_counting(self):
        session = self.env["event.session"].create(
            {
                "date_begin": "2017-05-27 20:00:00",
                "date_end": "2017-05-27 22:00:00",
                "event_id": self.event.id,
                "seats_limited": self.event.seats_limited,
                "seats_max": self.event.seats_max,
            }
        )
        atendee_1 = self.env["event.registration"].create(
            {
                "name": "First Atendee",
                "event_id": self.event.id,
                "session_id": session.id,
            }
        )
        atendee_2 = self.env["event.registration"].create(
            {
                "name": "Second Atendee",
                "event_id": self.event.id,
                "session_id": session.id,
            }
        )
        session._compute_seats()
        self.assertEqual(session.seats_unconfirmed, 2)
        self.assertEqual(session.seats_reserved, 0)
        atendee_1.action_confirm()
        session._compute_seats()
        self.assertEqual(session.seats_unconfirmed, 1)
        self.assertEqual(session.seats_reserved, 1)
        atendee_2.action_confirm()
        session._compute_seats()
        self.assertEqual(session.seats_unconfirmed, 0)
        self.assertEqual(session.seats_reserved, 2)
