# Copyright 2021 Camptocamp (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestRegistrationEditor(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.env["res.lang"].load_lang("fr_FR")
        cls.event_ticket = cls.env.ref("event_sale.event_0_ticket_1")
        cls.event = cls.event_ticket.event_id
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.env.ref("base.res_partner_2").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.event_ticket.product_id.id,
                            "price_unit": cls.event_ticket.price,
                            "product_uom": cls.event_ticket.product_id.uom_id.id,
                            "product_uom_qty": 1.0,
                            "event_id": cls.event.id,
                            "event_ticket_id": cls.event_ticket.id,
                        },
                    )
                ],
            }
        )
        cls.order.order_line._update_registrations()
        cls.registrations = cls.env["event.registration"].search(
            [("sale_order_id", "=", cls.order.id)]
        )

    def _get_registration_editor(self, order):
        return (
            self.env["registration.editor"]
            .with_context(active_model="sale.order", active_id=order.id)
            .create({})
        )

    def test_registration_editor_data(self):
        self.assertEqual(self.registrations.lang, "en_US")
        # Edit registration language
        wiz = self._get_registration_editor(self.order)
        self.assertEqual(wiz.event_registration_ids.lang, "en_US")
        wiz.event_registration_ids.lang = "fr_FR"
        wiz.action_make_registration()
        self.assertEqual(self.registrations.lang, "fr_FR")
