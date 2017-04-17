# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

"""Test permissions per user profile and model."""


from psycopg2 import IntegrityError
from . import test_permissions_bases as b
from openerp.tests.common import at_install


@at_install(True)
class UnprivilegedDurationTypePermissionsCase(b.UnprivilegedPermissionsCase,
                                              b.DurationTypePermissionsCase):
    pass


@at_install(True)
class UnprivilegedDurationPermissionsCase(b.UnprivilegedPermissionsCase,
                                          b.DurationPermissionsCase):
    pass


@at_install(True)
class UnprivilegedCourseTypePermissionsCase(b.UnprivilegedPermissionsCase,
                                            b.CourseTypePermissionsCase):
    pass


@at_install(True)
class UnprivilegedCoursePermissionsCase(b.UnprivilegedPermissionsCase,
                                        b.CoursePermissionsCase):
    pass


@at_install(True)
class UnprivilegedEventPermissionsCase(b.UnprivilegedPermissionsCase,
                                       b.EventPermissionsCase):
    pass


@at_install(True)
class UserDurationTypePermissionsCase(b.UserPermissionsCase,
                                      b.DurationTypePermissionsCase):
    pass


@at_install(True)
class UserDurationPermissionsCase(b.UserPermissionsCase,
                                  b.DurationPermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserDurationPermissionsCase, self).setUp(*args, **kwargs)

        # Expected exceptions
        self.ex_insert = None
        self.ex_update = None
        self.ex_delete = None


@at_install(True)
class UserCourseTypePermissionsCase(b.UserPermissionsCase,
                                    b.CourseTypePermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserCourseTypePermissionsCase, self).setUp(*args, **kwargs)


@at_install(True)
class UserCoursePermissionsCase(b.UserPermissionsCase,
                                b.CoursePermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserCoursePermissionsCase, self).setUp(*args, **kwargs)

        # Expected exceptions
        self.ex_insert = None
        self.ex_update = None
        self.ex_delete = None


@at_install(True)
class UserEventPermissionsCase(b.UserPermissionsCase,
                               b.EventPermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserEventPermissionsCase, self).setUp(*args, **kwargs)

        # Expected exceptions
        self.ex_insert = None
        self.ex_update = None
        self.ex_delete = None


@at_install(True)
class ManagerDurationTypePermissionsCase(b.ManagerPermissionsCase,
                                         b.DurationTypePermissionsCase):
    pass


@at_install(True)
class ManagerDurationPermissionsCase(b.ManagerPermissionsCase,
                                     b.DurationPermissionsCase):
    pass


@at_install(True)
class ManagerCourseTypePermissionsCase(b.ManagerPermissionsCase,
                                       b.CourseTypePermissionsCase):
    def setUp(self, *args, **kwargs):
        super(ManagerCourseTypePermissionsCase, self).setUp(*args, **kwargs)

        # This will fail because the manager deletes an course type that is a
        # FK to an course, and that's a required field
        self.ex_delete = IntegrityError


@at_install(True)
class ManagerCoursePermissionsCase(b.ManagerPermissionsCase,
                                   b.CoursePermissionsCase):
    pass


@at_install(True)
class ManagerEventPermissionsCase(b.ManagerPermissionsCase,
                                  b.EventPermissionsCase):
    pass
