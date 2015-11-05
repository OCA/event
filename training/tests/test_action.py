# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from .base import BaseCase, M


class ActionOperationsCase(BaseCase):
    """Test some record operations."""
    def setUp(self):
        super(ActionOperationsCase, self).setUp()
        # Add good duration types
        self.action.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[0].id,
             "action_id": self.action.id,
             "duration": 20.5})
        self.action.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[1].id,
             "action_id": self.action.id,
             "duration": 0.1})

    def test_copy_duration_ids(self):
        """Copy training action with durations."""
        # Copy the training action
        new = self.action.copy()

        # Check if durations were copied
        for field in ("duration", "type_id"):
            field = "duration_ids.%s" % field
            self.assertEqual(
                set(self.action.mapped(field)),
                set(new.mapped(field)),
                "Field %s differs." % field)

    def test_unlink(self):
        """Unlink training action with durations."""
        self.action.unlink()


class ActionOnChangeBaseCase(object):
    """Common methods for this module."""
    def tearDown(self, *args, **kwargs):
        """All tests end checking that the fulfill was right."""
        with self.env.do_in_onchange():
            # Set the action's type
            self.action.type_id = self.action_type_good

            # This should be run automatically when on UI
            self.action._onchange_type_id_fulfill_expected_duration_types()

        # User presses *Save*
        # See http://stackoverflow.com/a/33255577/1468388
        self.action.write(self.action._convert_to_write(self.action._cache))

        # Check that it was fulfilled right
        self.assertEqual(set(self.action.mapped("duration_ids.type_id.name")),
                         set(self.duration_types_good.mapped("name")))

        super(ActionOnChangeBaseCase, self).tearDown(*args, **kwargs)


class ActionOnChangeTypeFulfillExpectedDurationTypesCase(
        ActionOnChangeBaseCase, BaseCase):
    """Test method _onchange_type_id_fulfill_expected_duration_types().

    That method of training actions gets triggered when changing the action
    type, and is supposed to update the duration_ids field.
    """
    create_method = "new"

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


class ActionMixOnChangeCase(ActionOnChangeBaseCase, BaseCase):
    """Problems when mixing onchange and real database writes."""
    def test_when_editing_and_replacing_twice(self):
        """Action had duration X, then X autoremoved and X autoadded again.

        This test can fail **because we are in on change** mode.

        The on change trigger deletes an existing duration, and then creates a
        new one with the same unique key, and thus fails to save.
        """
        # Action has one duration written in DB
        self.action.duration_ids |= self.create(
            "duration",
            {"type_id": self.duration_types_good[0].id,
             "action_id": self.action.id,
             "duration": 20})

        self.create_method = "new"
        self.action = self.action.with_context(active_model=M % "action",
                                               active_id=self.action.id)
        with self.env.do_in_onchange():
            # The user changes the action type
            self.action.type_id = self.action_type_bad

            # The duration gets deleted
            self.action._onchange_type_id_fulfill_expected_duration_types()
