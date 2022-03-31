# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def button_cancel(self):
        super().button_cancel()
        if self.state == "cancel" and not self.env.context.get("is_merge", False):
            self.mapped("invoice_line_ids.sale_line_ids.registration_ids").filtered(
                lambda x: x.state not in ["done", "draft"]
            ).write({"state": "draft"})

    def unlink(self):
        registrations = self.mapped(
            "invoice_line_ids.sale_line_ids.registration_ids"
        ).filtered(lambda x: x.state not in ["done", "draft"])
        res = super().unlink()
        if res:
            registrations.filtered(lambda x: x.state not in ["done", "draft"]).write(
                {"state": "draft"}
            )

    def button_draft(self):
        super().button_draft()
        if self.state == "draft":
            self.mapped("invoice_line_ids.sale_line_ids.registration_ids").write(
                {"state": "draft"}
            )
