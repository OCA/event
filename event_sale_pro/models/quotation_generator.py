# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from .. import exceptions


class EventQuotationGenerator(models.TransientModel):
    _name = "event_sale_pro.quotation_generator"

    event_id = fields.Many2one(
        "event.event",
        "Event",
        readonly=True,
        default=lambda self: (self.env["event.registration"]
                              .browse(self.env.context.get("active_id"))
                              .event_id))
    event_type_id = fields.Many2one(
        string="Event type",
        readonly=True,
        related="event_id.type")
    product_id = fields.Many2one(
        "product.product",
        "Product",
        domain="""[("sale_ok", "=", True),
                   ("event_ok", "=", True),
                   ("event_type_id", "=", event_type_id)]""",
        help="Event subscription product that will be sold.")
    registration_ids = fields.Many2many(
        "event.registration",
        string="Registrations",
        relation="event_sale_pro_quotation_generator_registration_ids_rel",
        default=lambda self: self.env.context.get("active_ids"))
    group_by_commercial_entity = fields.Boolean(
        default=True,
        help="Check this box if you want to generate one quotation per "
             "commercial entity. Leave it unchecked to generate one per "
             "registration.")

    @api.multi
    def action_generate(self):
        """Generate sale orders for selected event registrations."""
        self.ensure_one()

        # Check that we are only working with one event
        if len(self.registration_ids.mapped("event_id")) > 1:
            raise exceptions.MultipleEventsError(
                _("You cannot generate quotations for multiple events."))

        orders = dict()
        for registration in self.registration_ids:
            # Get the client of the registration
            client = registration.invoiced_partner()
            if self.group_by_commercial_entity:
                client = client.commercial_partner_id

            # Create the sale order if it does not exist yet
            if client.id not in orders:
                orders[client.id] = self.create_quotation({
                    "origin": registration.event_id.name_get()[0][1],
                    "partner_id": client.id,
                })

            # New line in sale order
            line = self.create_quotation_line({
                "event_id": registration.event_id.id,
                "event_ticket_id": registration.event_ticket_id.id,
                "name": self.compute_description(registration),
                "order_id": orders[client.id].id,
                "product_id": self.product_id.id,
            })

            # Load ticket price
            line.update(
                line.onchange_event_ticket_id(
                    event_ticket_id=line.event_ticket_id.id)["value"])

            # Link it
            registration.origin_id = line

        return orders.values()

    @api.model
    @api.returns("sale.order")
    def create_quotation(self, data):
        """Create a sale order with the needed data."""
        return self.env["sale.order"].create(data)

    @api.model
    @api.returns("sale.order.line")
    def create_quotation_line(self, data):
        """Create a sale order line with the needed data."""
        return self.env["sale.order.line"].create(data)

    @api.multi
    def compute_description(self, registration):
        """Compute the product description for the sale order."""
        self.ensure_one()

        if registration.event_ticket_id:
            name = _('%(product)s in event "%(event)s" of type "%(type)s" '
                     'for %(partner)s.')
        else:
            name = _('%(product)s in event "%(event)s" for %(partner)s.')

        name = name % {
            "event": registration.event_id.name,
            "partner": registration.name or registration.partner_id.name,
            "product": self.product_id.name,
            "type": registration.event_ticket_id.name,
        }

        return name
