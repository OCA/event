# Copyright 2023 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class Product(models.Model):
    _inherit = "product.template"

    is_child_ticket = fields.Boolean(
        help="Child tickets can't be bought on website without buying a non child one."
    )
