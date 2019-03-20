# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_cancel(self):
        res = super(AccountInvoice, self).action_cancel()
        if res and not self.env.context.get('is_merge', False):
            self.mapped(
                'invoice_line_ids.sale_line_ids.registration_ids').filtered(
                lambda x: x.state not in ['done', 'draft']
            ).do_draft()
        return res

    @api.multi
    def unlink(self):
        registrations = self.mapped(
            'invoice_line_ids.sale_line_ids.registration_ids').filtered(
            lambda x: x.state not in ['done', 'draft'])
        res = super(AccountInvoice, self).unlink()
        if res:
            registrations.filtered(
                lambda x: x.state not in ['done', 'draft']).do_draft()

    @api.multi
    def action_invoice_draft(self):
        res = super(AccountInvoice, self).action_invoice_draft()
        if res:
            self._confirm_attendees()
