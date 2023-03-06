# Copyright 2017 Tecnativa - David Vidal
# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo.tests import Form, TransactionCase


class EventSaleSession(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_address_28")
        cls.product = cls.env.ref("event_sale.product_product_event")
        cls.session = cls.env.ref("event_session.event_session_007_1_16_00")
        cls.ticket = cls.env.ref("event_sale_session.event_ticket_007_standard")
        cls.event = cls.session.event_id
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "event_id": cls.event.id,
                            "event_session_id": cls.session.id,
                            "event_ticket_id": cls.ticket.id,
                            "product_uom_qty": 5.0,
                        },
                    ),
                ],
            }
        )

    def test_sale_session(self):
        """Sell an event with session"""
        self.order.action_confirm()
        regs = self.env["event.registration"].search(
            [("sale_order_id", "=", self.order.id)]
        )
        # Check that all registration data is properly set
        self.assertTrue(len(regs) > 0)
        for reg in regs:
            self.assertEqual(reg.event_id.id, self.event.id)
            self.assertEqual(reg.session_id.id, self.session.id)
            self.assertEqual(reg.partner_id.id, self.partner.id)
            self.assertEqual(reg.name, self.partner.name)
        # Check the event.session sale subtotal amount
        self.assertEqual(self.order.amount_untaxed, self.session.sale_price_subtotal)
        # Check that we can access the orders from the session
        action = self.session.action_view_linked_orders()
        orders = self.env["sale.order"].search(action["domain"])
        self.assertIn(self.order, orders)

    def test_sale_order_line_session_onchange_autocomplete(self):
        """Test that session is automatically filled and or unset on form"""
        form = Form(self.order)
        line = form.order_line.new()
        line.product_id = self.product
        # Case 1: The event is a session event, but has multiple sessions
        line.event_id = self.event
        self.assertFalse(line.event_session_id)
        # Case 2: The event is a session event with only 1 session
        (self.event.session_ids - self.session).active = False
        line.event_id = self.event
        self.assertEqual(line.event_session_id, self.session)
        # Case 3: The event is not a session event, session should be unset
        line.event_id = self.env.ref("event.event_0")
        self.assertFalse(line.event_session_id)

    def test_sale_order_event_configurator_onchange_autocomplete(self):
        """Test that session is automatically filled and or unset on wizard"""
        wizard = self.env["event.event.configurator"].create(
            {"product_id": self.product.id}
        )
        form = Form(wizard)
        # Case 1: The event is a session event, but has multiple sessions
        form.event_id = self.event
        self.assertFalse(form.event_session_id)
        # Case 2: The event is a session event with only 1 session
        (self.event.session_ids - self.session).active = False
        form.event_id = self.event
        self.assertEqual(form.event_session_id, self.session)
        # Case 3: The event is not a session event, session should be unset
        form.event_id = self.env.ref("event.event_0")
        self.assertFalse(form.event_session_id)

    def test_event_registration_editor(self):
        # Case 1: Read from sale.order.lines (event.registrations don't exist)
        editor = (
            self.env["registration.editor"]
            .with_context(default_sale_order_id=self.order.id)
            .create({})
        )
        self.assertEqual(len(editor.event_registration_ids), 5.0)
        self.assertEqual(
            editor.event_registration_ids.session_id,
            self.session,
            "Session is filled from sale.order.line",
        )
        # Case 2: Saving properly sets the session_id on event.registrations
        self.assertEqual(len(self.session.registration_ids), 0)
        editor.action_make_registration()
        self.assertEqual(len(self.session.registration_ids), 5)
        # Case 3: Read from event.registration
        editor = (
            self.env["registration.editor"]
            .with_context(default_sale_order_id=self.order.id)
            .create({})
        )
        self.assertEqual(len(editor.event_registration_ids), 5.0)
        self.assertEqual(
            editor.event_registration_ids.session_id,
            self.session,
            "Session is filled from event.registration",
        )
