# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo import fields
from odoo.tests import TransactionCase


class TestEventProject(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.organizer = cls.env["res.partner"].create({"name": "Organizer"})
        cls.date = {
            "begin": fields.Date.to_string(date.today()),
            "end": fields.Date.to_string(date.today() + timedelta(days=7)),
            "begin2": fields.Date.to_string(date.today() + timedelta(days=1)),
            "end2": fields.Date.to_string(date.today() + timedelta(days=9)),
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
                "date_begin": cls.date["begin"],
                "date_end": cls.date["end"],
                "project_id": cls.project.id,
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Task in project 2",
                "project_id": cls.project_2.id,
            }
        )

    def _link_project_to_event(self, event, project):
        """Set project in event"""
        event.write({"project_id": project.id})

    def _assert_event_project(self, event, project):
        """Assert a bunch of fields between event and project."""
        self.assertEqual(project.date, event.date_end.date())
        self.assertEqual(project.date_start, event.date_begin.date())
        self.assertEqual(project.name, event.display_name)
        self.assertEqual(project.partner_id, event.organizer_id)
        self.assertEqual(project.description, event.note)
        self.assertEqual(event.task_ids, project.task_ids)

    def test_initial_project(self):
        """Test when a project is linked to an event"""
        self._link_project_to_event(self.event, self.project)
        self._assert_event_project(self.event, self.project)

    def test_event_udpates(self):
        """Test project changes when event is updated"""
        self._link_project_to_event(self.event, self.project)
        self.event.date_begin = self.date["begin2"]
        self.event.date_end = self.date["end2"]
        self.event.name = "Event name changed"
        self.event.organizer_id = self.organizer
        self.event.note = "<p>Test note</p>"
        self._assert_event_project(self.event, self.project)

    def test_project_change(self):
        """Test project change in event"""
        self._link_project_to_event(self.event, self.project)
        self._assert_event_project(self.event, self.project)
        self.event.project_id = self.project_2
        self._assert_event_project(self.event, self.project_2)
