# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from psycopg2 import IntegrityError
from openerp import _, api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def button_confirm(self):
        """Add registrations to the already existing record if possible."""
        registrations = self.env["event.registration"]

        for s in self:
            try:
                with self.env.cr.savepoint():
                    super(SaleOrderLine, s).button_confirm()

            # A registration already exists
            except IntegrityError:
                match = registrations.search([
                    ("event_id", "=", s.event_id.id),
                    ("event_ticket_id", "=", s.event_ticket_id.id),
                    ("partner_id", "=", s.order_id.partner_id.id),
                ])
                qty = int(s.product_uom_qty)
                match.nb_register += qty
                match = match.with_context(mail_create_nolog=True)
                match.message_post(_("%d new registrations sold in %s.") %
                                   (qty, s.order_id.display_name))

        return True
