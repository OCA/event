# Copyright 2021 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class EventEventTicket(models.Model):
    _inherit = "event.event.ticket"

    def _get_ticket_combination_info(self):
        """Imitate product.template's _get_combination_info()."""
        # Obtain the inverse field of the normal b2b/b2c behavior
        alt_field = (
            "total_included"
            if self.env.user.has_group("account.group_show_line_subtotals_tax_excluded")
            else "total_excluded"
        )
        price, alt_price = self.price_reduce, self.price_reduce_taxinc
        # Inverse them if taxes excluded
        if alt_field == "total_excluded":
            price, alt_price = alt_price, price
        return {
            "alt_field": alt_field,
            "alt_list_price": alt_price,
            "alt_price": alt_price,
            "price": price,
            # HACK OPW-2518694: discounted price is always tax-excluded
            # TODO Check behavior when fixed
            "has_discounted_price": False,
        }
