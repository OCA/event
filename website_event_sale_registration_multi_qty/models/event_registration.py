# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _synchronize_so_line_values(self, so_line):
        result = super()._synchronize_so_line_values(so_line)
        if self.env.context.get("multi_qty_disable_sync"):
            result.pop("qty", False)
        return result

    def _get_website_registration_allowed_fields(self):
        return super()._get_website_registration_allowed_fields() | {"qty"}
