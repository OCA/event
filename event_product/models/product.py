# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from .. import exceptions as ex


class EventProductBase(models.AbstractModel):
    _name = "event_product.base"

    @api.multi
    @api.constrains("event_ok", "is_event")
    def _check_ticket_is_not_event(self):
        """Ensure events are not tickets."""
        for s in self:
            if s.event_ok and s.is_event:
                raise ex.EventAndTicketError()

    @api.multi
    @api.onchange("is_event")
    def _onchange_is_event(self):
        """Avoid conflicts between :attr:`~.event_ok` and :attr:`~.is_event`.

        Products cannot be an event and a ticket at the same time.
        """
        for s in self:
            if s.is_event:
                s.event_ok = False
                s.type = "service"


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "event_product.base"]

    is_event = fields.Boolean(
        "Is an event",
        help="This product defines an event (NOT an event ticket).")
    event_count = fields.Integer(
        "Events",
        compute="_compute_event_count")

    @api.multi
    @api.depends("product_variant_ids.event_ids")
    def _compute_event_count(self):
        """Count events related with template's variants."""
        for s in self:
            s.event_count = len(s.mapped("product_variant_ids.event_ids"))

    @api.multi
    @api.constrains("is_event", "event_type_id")
    def _check_event_type_consistent(self):
        """Avoid changing type if it creates an inconsistency."""
        self.product_variant_ids._check_event_type_consistent()

    @api.multi
    def onchange_event_ok(self, type, event_ok):
        """Inverse of :meth:`~._onchange_is_event`.

        Cannot declare in ``event_product.product`` because it gets ignored.
        """
        # TODO Merge with `_onchange_is_event` when core updates to new api
        result = super(ProductTemplate, self).onchange_event_ok(type, event_ok)
        if event_ok:
            result.setdefault("value", dict())
            result["value"]["is_event"] = False
        return result

    @api.multi
    def action_view_events(self):
        """Open events related to template's variants."""
        self.ensure_one()
        action = self.env.ref("event.action_event_view").read()[0]
        action["domain"] = [("product_id", "in", self.product_variant_ids.ids)]
        return action


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "event_product.base"]

    event_ids = fields.One2many(
        "event.event",
        "product_id",
        "Events")
    event_count = fields.Integer(
        "Events",
        compute="_compute_event_count")

    @api.multi
    @api.depends("event_ids")
    def _compute_event_count(self):
        """Count related events."""
        for s in self:
            s.event_count = len(s.event_ids)

    @api.multi
    @api.constrains("is_event", "event_type_id", "event_ids")
    def _check_event_type_consistent(self):
        """Avoid changing type if it creates an inconsistency."""
        self.mapped("event_ids")._check_product_type()

    @api.multi
    def onchange_event_ok(self, type, event_ok):
        """Inverse of :meth:`~._onchange_is_event`.

        Cannot declare in ``event_product.product`` because it gets ignored.
        """
        # TODO Merge with `_onchange_is_event` when core updates to new api
        result = super(ProductProduct, self).onchange_event_ok(type, event_ok)
        if event_ok:
            result.setdefault("value", dict())
            result["value"]["is_event"] = False
        return result

    @api.multi
    def action_view_events(self):
        """Open events related to product."""
        self.ensure_one()
        action = self.env.ref("event.action_event_view").read()[0]
        action["domain"] = [("product_id", "=", self.id)]
        return action
