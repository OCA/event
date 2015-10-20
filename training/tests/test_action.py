# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from .base import BaseCase


class ActionOnChangeTypeFulfillExpectedDurationTypesCase(BaseCase):
    """Test method _onchange_type_id_fulfill_expected_duration_types().

    That method of training actions gets triggered when changing the action
    type, and is supposed to update the duration_ids field.
    """

    create_method = "new"

    def tearDown(self, *args, **kwargs):
        """All tests end checking that the fulfill was right."""

        # Set the action's type
        self.action.type_id = self.action_type

        # This should be run automatically when on UI
        self.action._onchange_type_id_fulfill_expected_duration_types()

        # Check that it was fulfilled right
        self.assertEqual(set(self.action.mapped("duration_ids.type_id.name")),
                         set(self.duration_types_good.mapped("name")))

        (super(ActionOnChangeTypeFulfillExpectedDurationTypesCase, self)
         .tearDown(*args, **kwargs))

    def test_when_empty(self):
        """When training action has no duration records at all."""

        pass

    def test_when_full_good(self):
        """Create good duration records for the action."""

        for duration_type in self.duration_types_good:
            self.action.duration_ids |= self.create(
                "duration",
                {"type_id": duration_type.id,
                 "action_id": self.action.id})

    def test_when_half_good(self):
        """Create only one good duration record for the action."""

        self.action.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[0].id,
             "action_id": self.action.id})

    def test_when_full_bad(self):
        """Create bad duration records for the action."""

        for duration_type in self.duration_types_bad:
            self.action.duration_ids |= self.create(
                "duration",
                {"type_id": duration_type.id,
                 "action_id": self.action.id})

    def test_when_half_bad(self):
        """Create only one bad duration record for the action."""

        self.action.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_bad[0].id,
             "action_id": self.action.id})

    def test_when_half_good_half_bad(self):
        """Create only one good and one bad duration record for the action."""

        self.action.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[0].id,
             "action_id": self.action.id})
        self.action.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_bad[0].id,
             "action_id": self.action.id})
