# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import BaseCase


class RegistrationFromOrderCase(BaseCase):
    """Check registrations created from sales orders."""
    def test_origin(self):
        """Upstream origin field handling."""
        # Create a sale order line
        line = self.create_line()[0]
        line.button_confirm()

        # Check it created the correct registrations
        reg = self.event.registration_ids
        self.assertEqual(len(reg), 1)
        self.assertEqual(reg.partner_id, self.partner_1)
        self.assertEqual(reg.origin, self.sale_order.name)
        self.assertEqual(reg.origin_id, self.sale_order)
