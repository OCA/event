# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    deliverable_product_ids = fields.Many2many(
        "product.product",
        string="Products to deliver",
        domain=[("is_event", "=", False)],
        help="These should be delivered to every attendee.")

    @api.multi
    def action_load_deliverable_products(self):
        """Load products to deliver from the linked product."""
        for s in self:
            s.deliverable_product_ids = (
                s.product_id.event_deliverable_product_ids)

    @api.multi
    def action_products_delivered_to_all(self):
        """Mark all products delivered to all attendees."""
        self.mapped("registration_ids").write({"products_delivered": True})

    @api.multi
    @api.onchange("deliverable_product_ids")
    def _onchange_deliverable_product_ids(self):
        """Warn if products were already delivered."""
        if True in self.mapped("registration_ids.products_delivered"):
            raise exceptions.Warning(
                _("Some products were already delivered."))


class EventRegistration(models.Model):
    _inherit = "event.registration"

    products_delivered = fields.Boolean(
        help="Have products been delivered to this attendee?")

    @api.constrains("products_delivered")
    def _check_products_delivered(self):
        """Cannot deliver products if no products are set."""
        for s in self:
            if s.products_delivered and not s.event_id.deliverable_product_ids:
                raise exceptions.ValidationError(
                    _("Event has no products set to deliver."))
