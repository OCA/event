# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models
from openerp.addons.event_registration_partner_unique import exceptions


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def button_confirm(self):
        """Add registrations to the already existing record if possible."""
        for s in self:
            try:
                with self.env.cr.savepoint():
                    super(SaleOrderLine, s).button_confirm()

            # A registration already exists
            except exceptions.DuplicatedPartnerError as error:
                regs = error._kwargs["registrations"].with_context(
                    mail_create_nolog=True)
                qty = int(s.product_uom_qty)
                for reg in regs:
                    reg.nb_register += qty
                regs.message_post(_("%d new registrations sold in %s.") %
                                  (qty, s.order_id.display_name))

        return True
