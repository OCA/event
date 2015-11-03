# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

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
class UnprivilegedActionTypePermissionsCase(b.UnprivilegedPermissionsCase,
                                            b.ActionTypePermissionsCase):
    pass


@at_install(True)
class UnprivilegedActionPermissionsCase(b.UnprivilegedPermissionsCase,
                                        b.ActionPermissionsCase):
    pass


@at_install(True)
class UnprivilegedMaterialTypePermissionsCase(b.UnprivilegedPermissionsCase,
                                              b.MaterialTypePermissionsCase):
    pass


@at_install(True)
class UnprivilegedMaterialPermissionsCase(b.UnprivilegedPermissionsCase,
                                          b.MaterialPermissionsCase):
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
class UserActionTypePermissionsCase(b.UserPermissionsCase,
                                    b.ActionTypePermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserActionTypePermissionsCase, self).setUp(*args, **kwargs)


@at_install(True)
class UserActionPermissionsCase(b.UserPermissionsCase,
                                b.ActionPermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserActionPermissionsCase, self).setUp(*args, **kwargs)

        # Expected exceptions
        self.ex_insert = None
        self.ex_update = None
        self.ex_delete = None


@at_install(True)
class UserMaterialTypePermissionsCase(b.UserPermissionsCase,
                                      b.MaterialTypePermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserMaterialTypePermissionsCase, self).setUp(*args, **kwargs)


@at_install(True)
class UserMaterialPermissionsCase(b.UserPermissionsCase,
                                  b.MaterialPermissionsCase):
    def setUp(self, *args, **kwargs):
        super(UserMaterialPermissionsCase, self).setUp(*args, **kwargs)


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
class ManagerActionTypePermissionsCase(b.ManagerPermissionsCase,
                                       b.ActionTypePermissionsCase):
    def setUp(self, *args, **kwargs):
        super(ManagerActionTypePermissionsCase, self).setUp(*args, **kwargs)

        # This will fail because the manager deletes an action type that is a
        # FK to an action, and that's a required field
        self.ex_delete = IntegrityError


@at_install(True)
class ManagerActionPermissionsCase(b.ManagerPermissionsCase,
                                   b.ActionPermissionsCase):
    pass


@at_install(True)
class ManagerMaterialTypePermissionsCase(b.ManagerPermissionsCase,
                                         b.MaterialTypePermissionsCase):
    def setUp(self, *args, **kwargs):
        super(ManagerMaterialTypePermissionsCase, self).setUp(*args, **kwargs)

        self.ex_delete = IntegrityError


@at_install(True)
class ManagerMaterialPermissionsCase(b.ManagerPermissionsCase,
                                     b.MaterialPermissionsCase):
    pass


@at_install(True)
class ManagerEventPermissionsCase(b.ManagerPermissionsCase,
                                  b.EventPermissionsCase):
    pass
