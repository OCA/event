# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from .. import exceptions as ex


class EventEvent(models.Model):
    _inherit = "event.event"

    product_id = fields.Many2one(
        "product.product",
        "Product",
        domain="""[("is_event", "=", True),
                   ("event_type_id", "in", (False, type))]""",
        states={"done": [("readonly", True)]},
        help="Product of this event, if available.")

    @api.multi
    @api.constrains("type", "product_id")
    def _check_product_type(self):
        """Ensure product and event types match."""
        for s in self.filtered("product_id"):
            if not s.product_id.is_event:
                raise ex.ProductIsNotEventError(s.product_id.display_name)
            elif (s.product_id.event_type_id and
                  s.product_id.event_type_id != s.type):
                raise ex.TypeMismatchError(
                    product_type=s.product_id.event_type_id.display_name,
                    event_type=s.type.display_name)

    @api.multi
    @api.onchange("type")
    def _onchange_type_clear_product(self):
        """Better have no product than have a wrong one."""
        for s in self:
            try:
                s._check_product_type()
            except ex.TypeMismatchError:
                s.product_id = False
