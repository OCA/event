# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from openerp.addons.event_sale.event_sale import sale_order_line


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.one
    def button_confirm(self):
        """Skip creation of registration if this is created from it.

        Now, registrations can be used to create sale order lines, so when
        that happens, there is no need to create them again.
        """
        # Check if there exists a registration linked to this order line
        matching_registrations = (
            self.env["event.registration"]
            .search([("origin_id", "=", "%s,%d" % (self._name, self.id))]))

        # Skip event_sale if so
        class_ = sale_order_line if matching_registrations else SaleOrderLine

        # Add a default value for event.registration.origin_line_id, useful
        # if class_ is SaleOrderLine
        instance = self.with_context(default_origin_line_id=self.id)

        return super(class_, instance).button_confirm()
