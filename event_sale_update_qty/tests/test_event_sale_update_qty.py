# Copyright 2026 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import tagged

from odoo.addons.event_sale.tests.common import TestEventSaleCommon


@tagged("post_install", "-at_install")
class TestEventSaleUpdateQty(TestEventSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Attendee",
                "email": "attendee@example.com",
                "phone": "+34600000000",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Event Ticket",
                "type": "service",
                "service_tracking": "event",
                "taxes_id": False,
            }
        )
        cls.ticket = cls.env["event.event.ticket"].create(
            {
                "name": "Standard Ticket",
                "event_id": cls.event_0.id,
                "product_id": cls.product.id,
                "price": 10.0,
            }
        )
        cls.sale_order = cls.env["sale.order"].create({"partner_id": cls.partner.id})
        cls.sale_order_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.product.id,
                "product_uom_qty": 3,
                "event_id": cls.event_0.id,
                "event_ticket_id": cls.ticket.id,
                "price_unit": 10.0,
            }
        )
        cls.sale_order.action_confirm()
        cls.env["registration.editor"].with_context(
            default_sale_order_id=cls.sale_order.id
        ).create({}).action_make_registration()

    def _create_update_wizard(self, new_qty, registrations=None):
        values = {
            "sale_order_line_id": self.sale_order_line.id,
            "new_qty": new_qty,
        }
        if registrations:
            values["registration_ids"] = [Command.set(registrations.ids)]
        return self.env["event.sale.update.qty.wizard"].create(values)

    def test_reduce_quantity(self):
        registrations = self.sale_order_line.registration_ids
        registrations_to_remove = registrations[:2]
        remaining_registration = registrations - registrations_to_remove
        wizard = self._create_update_wizard(1, registrations_to_remove)
        result = wizard.action_update()
        self.assertEqual(result, {"type": "ir.actions.client", "tag": "soft_reload"})
        self.assertEqual(self.sale_order_line.product_uom_qty, 1)
        self.assertFalse(registrations_to_remove.exists())
        self.assertEqual(self.sale_order_line.registration_ids, remaining_registration)

    def test_increase_quantity(self):
        previous_registrations = self.sale_order_line.registration_ids
        wizard = self._create_update_wizard(5)
        wizard.action_update()
        self.assertEqual(self.sale_order_line.product_uom_qty, 5)
        self.assertEqual(len(self.sale_order_line.registration_ids), 5)
        new_registrations = (
            self.sale_order_line.registration_ids - previous_registrations
        )
        self.assertEqual(len(new_registrations), 2)
