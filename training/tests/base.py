# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from datetime import datetime
from openerp.tests.common import TransactionCase
from ..models.common import M


class BaseCase(TransactionCase):
    """Common setup methods."""
    create_method = "create"

    def create(self, model, values):
        """Create a new record in the given model with the given values."""

        if "." not in model:
            model = M % model

        return getattr(self.env[model], self.create_method)(values)

    def setUp(self):
        """Create dummy data to work with."""

        super(BaseCase, self).setUp()

        self.event = self.create(
            "event.event",
            {"name": "Dummy training group event",
             "date_begin": datetime.now(),
             "date_end": datetime.now()})

        self.action_type_good = self.create(
            "action_type",
            {"name": "Dummy good training action type"})

        self.action_type_bad = self.create(
            "action_type",
            {"name": "Dummy bad training action type"})

        self.action = self.create(
            "action",
            {"name": "Dummy training action",
             "type_id": self.action_type_good.id})

        duration_type_1 = self.create(
            "duration_type",
            {"name": "Dummy duration type 1 (good)"})

        duration_type_2 = self.create(
            "duration_type",
            {"name": "Dummy duration type 2 (good)"})

        duration_type_3 = self.create(
            "duration_type",
            {"name": "Dummy duration type 3 (bad)"})

        duration_type_4 = self.create(
            "duration_type",
            {"name": "Dummy duration type 4 (bad)"})

        self.duration_types_good = duration_type_1 | duration_type_2
        self.duration_types_bad = duration_type_3 | duration_type_4

        self.action_type_good.expected_duration_type_ids = (
            self.duration_types_good)
        self.action_type_bad.expected_duration_type_ids = (
            self.duration_types_bad)

        self.student_1 = self.create(
            "res.partner",
            {"name": "Dummy student 1"})

        self.student_2 = self.create(
            "res.partner",
            {"name": "Dummy student 2"})

        self.students = self.student_1 | self.student_2

        self.manager = self.create(
            "res.users",
            {"name": "Manager user",
             "login": "manager_user"})
        self.manager.groups_id |= self.env.ref(M % "manager_group")

        self.user = self.create(
            "res.users",
            {"name": "Training user",
             "login": "training_user"})
        self.user.groups_id |= self.env.ref(M % "user_group")

        self.unprivileged = self.create(
            "res.users",
            {"name": "Mr. Nobody",
             "login": "unprivileged"})

        self.material_1 = self.create(
            "material",
            {"name": "Material 1",
             "type_id": self.env.ref("training.material_type_physical").id})
        self.material_2 = self.create(
            "material",
            {"name": "Material 2",
             "type_id": self.env.ref("training.material_type_electronic").id})
        self.materials = self.material_1 | self.material_2
