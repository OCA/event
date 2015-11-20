# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

"""Base classes for testing permissions.

There is one base class per model and another per user profile.
Combine them to make the tests.
"""

from .base import BaseCase, M
from openerp import exceptions as e
from openerp.tests.common import at_install


# Base class for all tests. Don't run tests in this module.
@at_install(False)
class PermissionsCase(BaseCase):
    """Test permissions for reading, creating, editing, deleting.

    Base class for permissions tests.
    """
    def setUp(self, *args, **kwargs):
        """Change user to test permissions.

        Also prepare the variables needed to run the tests.
        """
        # Create standard records
        super(PermissionsCase, self).setUp(*args, **kwargs)

        # Parameters that will be used for running tests
        self.tested_user = None
        self.tested_record = None
        self.subtest = None
        self.insert_data = {"name": str(self)}

        # Expected exceptions
        self.ex_select = e.AccessError
        self.ex_insert = e.AccessError
        self.ex_update = e.AccessError
        self.ex_delete = e.AccessError

    def tearDown(self, *args, **kwargs):
        """Check expected exception (if there is one)."""
        # Test that the method raises the right exception, if any
        method = (self.assertRaises
                  if self.expected_exception
                  else lambda ex, test: test())

        # Ensure you always close the cursor
        try:
            method(self.expected_exception, self.subtest)
        finally:
            super(PermissionsCase, self).tearDown(*args, **kwargs)

    def _sudo(self):
        """Use the given model with the given user."""
        return self.env[self.tested_record._name].sudo(self.tested_user)

    def test_select(self):
        "Test permissions when reading a record."
        self.expected_exception = self.ex_select
        self.subtest = lambda: getattr(
            self._sudo().browse(self.tested_record.id),
            self.insert_data.keys()[0])

    def test_update(self):
        "Test permissions when updating a record."
        self.expected_exception = self.ex_update
        self.subtest = lambda: (self._sudo().browse(self.tested_record.id)
                                .write(self.insert_data))

    def test_insert(self):
        "Test permissions when inserting a record."
        self.expected_exception = self.ex_insert
        self.tested_user.email = "example@example.com"
        self.subtest = lambda: self._sudo().create(self.insert_data)

    def test_delete(self):
        "Test permissions when deleting a record."
        self.expected_exception = self.ex_delete
        self.subtest = lambda: (self._sudo()
                                .browse(self.tested_record.id).unlink())


# Base classes per model
class DurationTypePermissionsCase(PermissionsCase):
    def setUp(self, *args, **kwargs):
        super(DurationTypePermissionsCase, self).setUp(*args, **kwargs)

        self.tested_record = self.duration_types_good[0]


class DurationPermissionsCase(PermissionsCase):
    def setUp(self, *args, **kwargs):
        super(DurationPermissionsCase, self).setUp(*args, **kwargs)

        self.insert_data = {"type_id": self.duration_types_good[0].id,
                            "course_id": self.course.id}
        self.tested_record = self.create(M % "duration", self.insert_data)
        self.insert_data["type_id"] = self.duration_types_good[1].id


class CourseTypePermissionsCase(PermissionsCase):
    def setUp(self, *args, **kwargs):
        super(CourseTypePermissionsCase, self).setUp(*args, **kwargs)

        self.tested_record = self.course_type_good


class CoursePermissionsCase(PermissionsCase):
    def setUp(self, *args, **kwargs):
        super(CoursePermissionsCase, self).setUp(*args, **kwargs)

        self.tested_record = self.course
        self.insert_data["type_id"] = self.course_type_good.id


class EventPermissionsCase(PermissionsCase):
    def setUp(self, *args, **kwargs):
        super(EventPermissionsCase, self).setUp(*args, **kwargs)

        self.tested_record = self.event
        self.insert_data["date_begin"] = self.event.date_begin
        self.insert_data["date_end"] = self.event.date_end

        # Even unprivileged users can access events.
        # This may be a problem, but it's outside the scope of this module.
        self.ex_select = None


# Base classes per user
class UnprivilegedPermissionsCase(PermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UnprivilegedPermissionsCase, self).setUp(*args, **kwargs)

        self.tested_user = self.unprivileged


class UserPermissionsCase(PermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserPermissionsCase, self).setUp(*args, **kwargs)

        self.tested_user = self.user

        # Expected exceptions
        self.ex_select = None


class ManagerPermissionsCase(PermissionsCase):
    def setUp(self, *args, **kwargs):
        super(ManagerPermissionsCase, self).setUp(*args, **kwargs)

        self.tested_user = self.manager

        # Expected exceptions
        self.ex_select = None
        self.ex_insert = None
        self.ex_update = None
        self.ex_delete = None
