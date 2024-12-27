# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import psycopg2
from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests.common import TransactionCase, users
from odoo.tools import mute_logger

from odoo.addons.mail.tests.common import mail_new_test_user as new_test_user


class TestEventProject(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        new_test_user(
            cls.env,
            login="test-event_manager_user",
            groups="base.group_user,event.group_event_manager",
            notification_type="inbox",
        )
        cls.organizer = cls.env["res.partner"].create({"name": "Organizer"})
        current_time = fields.Datetime.now()
        cls.event_dates = {
            "begin": current_time,
            "end": current_time + relativedelta(days=7),
            "begin2": current_time + relativedelta(days=1),
            "end2": current_time + relativedelta(days=9),
        }
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test project",
            }
        )
        cls.project_2 = cls.env["project.project"].create(
            {
                "name": "Test project 2",
            }
        )
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event with project",
                "date_begin": cls.event_dates["begin"],
                "date_end": cls.event_dates["end"],
            }
        )
        cls.event_2 = cls.env["event.event"].create(
            {
                "name": "Test event 2",
                "date_begin": cls.event_dates["begin2"],
                "date_end": cls.event_dates["end2"],
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Task in project 2",
                "project_id": cls.project_2.id,
            }
        )
        cls.event.project_id = cls.project.id

    @users("test-event_manager_user")
    def _assert_project_event(self, project):
        """Assert a bunch of fields between event and project."""
        self.assertEqual(project.name, self.event.display_name)
        self.assertEqual(project.date_start, self.event.date_begin.date())
        self.assertEqual(project.date, self.event.date_end.date())
        self.assertEqual(project.partner_id, self.event.organizer_id)
        self.assertEqual(project.description, self.event.note)
        self.assertEqual(project.task_ids, self.event.task_ids)

    @users("test-event_manager_user")
    def test_initial_project(self):
        """Test when a project is linked to an event"""
        self._assert_project_event(self.project)

    @users("test-event_manager_user")
    def test_event_udpates(self):
        """Test project changes when event is updated"""
        self.event.date_begin = self.event_dates["begin2"]
        self.event.date_end = self.event_dates["end2"]
        self.event.name = "Event name changed"
        self.event.organizer_id = self.organizer.id
        self.event.note = "<p>Test note</p>"
        self._assert_project_event(self.project)

    @users("test-event_manager_user")
    def test_project_change(self):
        """Test project change in event"""
        self.event.project_id = self.project_2
        self._assert_project_event(self.project_2)

    @users("test-event_manager_user")
    def test_same_project_for_events(self):
        """Test project change in event"""
        with (
            mute_logger("odoo.sql_db"),
            self.assertRaises(psycopg2.errors.UniqueViolation),
            self.cr.savepoint(),
        ):
            self.event_2.project_id = self.project
