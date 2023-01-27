# Copyright 2021 Tecnativa - Jairo Llopis
# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime, timedelta

from odoo.tests.common import Form, TransactionCase

from ..exceptions import ReservationWithoutEventTypeError


class EventSaleCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        qtys = (1, 10, 100)
        cls.event_types = cls.env["event.type"].create(
            [{"name": "event type %d" % num} for num in range(3)]
        )
        cls.products = cls.env["product.product"].create(
            [
                {
                    "detailed_type": "event_reservation",
                    "event_reservation_type_id": cls.event_types[num].id,
                    "list_price": num,
                    "name": "product reservation for event type %d" % num,
                }
                for num in range(3)
            ]
        )
        cls.events = cls.env["event.event"].create(
            [
                {
                    "date_begin": datetime.now(),
                    "date_end": datetime.now() + timedelta(days=1),
                    "event_ticket_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "ticket %d" % num,
                                "product_id": cls.products[num].id,
                            },
                        )
                    ],
                    "event_type_id": cls.event_types[num].id,
                    "name": "event %d" % num,
                }
                for num in range(3)
            ]
        )
        cls.customers = cls.env["res.partner"].create(
            [
                {
                    "email": "%d@example.com" % num,
                    "name": "customer %d" % num,
                    "phone": num,
                }
                for num in range(3)
            ]
        )
        cls.orders = cls.env["sale.order"].create(
            [
                {
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": cls.products[num].id,
                                "product_uom_qty": qtys[num],
                            },
                        ),
                    ],
                    "partner_id": cls.customers[num].id,
                }
                for num in range(3)
            ]
        )

    def wizard_reservation_to_registration(self, order):
        """Generate a wizard to register reservations."""
        return Form(
            self.env["registration.editor"].with_context(
                active_id=order.id,
                active_ids=order.ids,
                active_model=order._name,
                registering_reservations=True,
            ),
            view="event_sale_reservation.registration_editor_reservations_view_form",
        )

    def wizard_step_2(self, wizard1):
        """Generate a step 2 wizard from the step 1 wizard."""
        multi_action = wizard1.action_convert_to_registration()
        # Ensure we first close the first wizard
        self.assertEqual(multi_action["type"], "ir.actions.act_multi")
        self.assertEqual(
            multi_action["actions"][0]["type"], "ir.actions.act_window_close"
        )
        # Get form from 2nd chained action
        action = multi_action["actions"][1]
        return Form(
            self.env[action["res_model"]].with_context(**action["context"]),
            view=action["view_id"],
        )

    def test_wrong_product_reservation_without_type(self):
        """Event reservation products require the type."""
        with self.assertRaises(ReservationWithoutEventTypeError):
            self.env["product.product"].create(
                {
                    "detailed_type": "event_reservation",
                    "list_price": 10,
                    "name": "event reservation without event type fails",
                }
            )

    def test_event_type_open_orders(self):
        """Test the smart button that opens orders from an event type."""
        self.orders.action_confirm()
        groups = zip(self.event_types, self.orders, (1, 10, 100))
        for ev_type, so, reservations in groups:
            self.assertEqual(ev_type.seats_reservation_total, reservations)
            action = ev_type.action_open_sale_orders()
            found_so = self.env[action["res_model"]].search(action["domain"])
            self.assertEqual(found_so, so)

    def test_sale_workflow(self):
        # Start: orders are draft, all is pending, nothing is reserved
        self.orders.invalidate_cache(["event_reservations_pending"])
        self.assertEqual(self.orders.mapped("event_reservations_pending"), [1, 10, 100])
        self.assertEqual(self.event_types.mapped("seats_reservation_total"), [0, 0, 0])
        # Confirm orders: all is pending, all is reserved
        self.orders.action_confirm()
        self.orders.invalidate_cache(["event_reservations_pending"])
        self.assertEqual(self.orders.mapped("event_reservations_pending"), [1, 10, 100])
        self.assertEqual(
            self.event_types.mapped("seats_reservation_total"), [1, 10, 100]
        )
        # Register 2nd SO to event using wizard
        wiz1 = self.wizard_reservation_to_registration(self.orders[1])
        self.assertEqual(len(wiz1.event_registration_ids), 1)
        wiz1_line = wiz1.event_registration_ids.edit(0)
        wiz1_line.event_id = self.events[1]
        wiz1_line.event_ticket_id = self.events[1].event_ticket_ids
        wiz1_line.save()
        # Click "Next": opens 2nd wizard to configure registrations
        wiz2 = self.wizard_step_2(wiz1.save())
        self.assertEqual(len(wiz2.event_registration_ids), 10)
        for num in range(len(wiz2.event_registration_ids)):
            wiz2_line = wiz2.event_registration_ids.edit(num)
            wiz2_line.name = "name %d" % num
            wiz2_line.email = "%d@example.com" % num
            wiz2_line.phone = "phone %d" % num
            wiz2_line.save()
        wiz2.save().action_make_registration()
        # 1st and 3rd SO are pending and reserved
        self.orders.invalidate_cache(["event_reservations_pending"])
        self.assertEqual(self.orders.mapped("event_reservations_pending"), [1, 0, 100])
        self.assertEqual(
            self.event_types.mapped("seats_reservation_total"), [1, 0, 100]
        )
