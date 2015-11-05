# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from .base import BaseCase, M
from .. import exceptions as ex


class GradeCase(BaseCase):
    def setUp(self):
        super(GradeCase, self).setUp()
        self.event.training_action_id = self.action

        for student in self.students:
            self.event.registration_ids |= self.create(
                "event.registration",
                {"partner_id": student.id,
                 "event_id": self.event.id})

        self.event.registration_ids.write({
            "grade": 5,
        })
        self.action_2 = self.create(
            M % "action",
            {"name": "Training action 2",
             "type_id": self.action_type_good.id})
        self.reg = self.event.registration_ids[0]

    def test_grade_min_above_max(self):
        """Block setting minimum grade above maximum."""
        with self.assertRaises(ex.GradeLimitIncoherentError):
            self.action.grade_min = self.action.grade_max + 0.01

    def test_grade_max_below_min(self):
        """Block setting maximum grade below minimum."""
        with self.assertRaises(ex.GradeLimitIncoherentError):
            self.action.grade_max = self.action.grade_min - 0.01

    def test_grade_pass_above_max(self):
        """Block setting passing grade above maximum."""
        with self.assertRaises(ex.GradeLimitIncoherentError):
            self.action.grade_pass = self.action.grade_max + 0.01

    def test_grade_pass_below_min(self):
        """Block setting passing grade below minimum."""
        with self.assertRaises(ex.GradeLimitIncoherentError):
            self.action.grade_pass = self.action.grade_min - 0.01

    def test_grade_pass_equal_limits(self):
        """Passing grade can be equal to maximum or minimum."""
        self.action.grade_pass = self.action.grade_min
        self.action.grade_pass = self.action.grade_max

    def test_grade_equals_limits(self):
        """Registration gets grade equal to limits.

        Just to ensure ``<=`` is being used and not ``<`` for constraints.
        """
        self.reg.grade = self.action.grade_min
        self.reg.grade = self.action.grade_pass
        self.reg.grade = self.action.grade_max

    def test_grade_below_limit(self):
        """Registration gets grade below allowed limit."""
        with self.assertRaises(ex.GradeLimitError):
            self.reg.grade = -0.5

    def test_grade_above_limit(self):
        """Registration gets grade above allowed limit."""
        with self.assertRaises(ex.GradeLimitError):
            self.reg.grade = 10.5

    def test_passing(self):
        """Test if student passes or not according to its grade."""
        # Grade 5 by default
        self.assertTrue(self.reg.passing)
        self.reg.grade -= 0.01
        self.assertFalse(self.reg.passing)

    def test_grade_min_change(self):
        """Changing minimum grade is blocked if there are conflicts."""
        self.action.grade_pass = 7
        with self.assertRaises(ex.GradeLimitError):
            self.action.grade_min = 5.01

    def test_grade_max_change(self):
        """Changing maximum grade is blocked if there are conflicts."""
        self.action.grade_pass = 3
        with self.assertRaises(ex.GradeLimitError):
            self.action.grade_max = 4.09

    def test_grade_pass_change(self):
        """Changing passing grade changes status in registrations."""
        self.action.grade_pass = 5.01
        self.assertFalse(self.reg.passing)

        self.action.grade_pass = 4.09
        self.assertTrue(self.reg.passing)

    def test_grade_min_change_action(self):
        """Changing action is blocked if minimum grade conflicts."""
        self.action_2.grade_pass = 7
        self.action_2.grade_min = 5.01
        with self.assertRaises(ex.GradeLimitError):
            self.event.training_action_id = self.action_2

    def test_grade_max_change_action(self):
        """Changing action is blocked if maximum grade conflicts."""
        self.action_2.grade_pass = 3
        self.action_2.grade_max = 4.09
        with self.assertRaises(ex.GradeLimitError):
            self.event.training_action_id = self.action_2

    def test_grade_pass_change_action(self):
        """Changing action with other passing grade changes registrations."""
        self.action_2.grade_pass = 5.01
        self.event.training_action_id = self.action_2
        self.assertFalse(self.reg.passing)

        self.action.grade_pass = 4.09
        self.event.training_action_id = self.action
        self.assertTrue(self.reg.passing)
