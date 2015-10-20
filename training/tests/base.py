# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from datetime import datetime
from openerp.tests.common import TransactionCase
from ..models import _D


class BaseCase(TransactionCase):
    """Common setup methods."""

    create_method = "create"

    def create(self, model, values):
        """Create a new record in the given model with the given values."""

        if "." not in model:
            model = _D % model

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

        tutor_1 = self.create(
            "res.partner",
            {"name": "Dummy tutuor 1"})

        tutor_2 = self.create(
            "res.partner",
            {"name": "Dummy tutuor 2"})

        self.tutors = tutor_1 | tutor_2

        self.manager = self.create(
            "res.users",
            {"name": "Manager user",
             "login": "manager_user"})
        self.manager.groups_id |= self.env.ref("training.manager_group")

        self.user = self.create(
            "res.users",
            {"name": "Training user",
             "login": "training_user"})
        self.user.groups_id |= self.env.ref("training.user_group")

        self.unprivileged = self.create(
            "res.users",
            {"name": "Mr. Nobody",
             "login": "unprivileged"})
