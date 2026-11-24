# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.http import request

from odoo.addons.base_rest.controllers.main import _PseudoCollection
from odoo.addons.base_rest.tests.common import BaseRestCase
from odoo.addons.component.core import WorkContext
from odoo.addons.extendable.tests.common import ExtendableMixin


class EventCase(BaseRestCase, ExtendableMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        collection = _PseudoCollection("event.rest.services", cls.env)
        cls.services_env = WorkContext(
            model_name="rest.service.registration",
            collection=collection,
            request=request,
        )
        cls.service = cls.services_env.component(usage="event")
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test Event",
                "date_begin": datetime.now(),
                "date_end": datetime.now(),
            }
        )
        cls.setUpExtendable()

    # pylint: disable=W8106
    def setUp(self):
        # resolve an inheritance issue (common.TransactionCase does not call
        # super)
        BaseRestCase.setUp(self)
        ExtendableMixin.setUp(self)

    def test_get_event(self):
        res = self.service.dispatch("get", self.event.id)
        self.assertEqual(res["name"], "Test Event")
