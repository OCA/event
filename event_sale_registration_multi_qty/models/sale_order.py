# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _update_registrations(self, confirm=True, registration_data=None):
        """ Writes registrations """
        Registration = self.env['event.registration']
        registrations = Registration.search([
            ('sale_order_line_id', 'in', self.ids)
        ])
        for so_line in self.filtered('event_id'):
            if not so_line.event_id.registration_multi_qty:
                super(SaleOrderLine, so_line)._update_registrations()
                continue
            existing_registrations = registrations.filtered(
                lambda self: self.sale_order_line_id.id == so_line.id)
            if confirm:
                existing_registrations.filtered(
                    lambda self: self.state != 'open'
                ).confirm_registration()
            else:
                existing_registrations.filtered(
                    lambda self: self.state == 'cancel').do_draft()
            registration = {}
            if registration_data:
                registration = registration_data.pop()
            if not existing_registrations:
                registration['sale_order_line_id'] = so_line
                registration['qty'] = int(so_line.product_uom_qty)
                Registration.with_context(
                    registration_force_draft=True).create(
                    Registration._prepare_attendee_values(registration))
        return True
