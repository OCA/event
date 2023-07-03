# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    website_event_sale_constraints_message = fields.Text(
        default="Please add at least one parent ticket to be able to register.",
    )
