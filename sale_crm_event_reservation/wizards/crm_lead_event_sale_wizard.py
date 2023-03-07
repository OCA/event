# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tests.common import Form


class CRMLeadEventSale(models.TransientModel):
    _name = "crm.lead.event.sale.wizard"
    _description = "Wizard to generate event quotation from event opportunity"

    opportunity_id = fields.Many2one(
        comodel_name="crm.lead",
        index=True,
        ondelete="cascade",
        readonly=True,
        required=True,
        string="Opportunity",
    )
    event_type_id = fields.Many2one(
        readonly=True,
        related="opportunity_id.event_type_id",
    )
    mode = fields.Selection(
        required=True,
        selection=[
            ("register", "Register in scheduled event"),
            ("reserve", "Reserve upcoming event"),
        ],
        help="How to create the event quotation?",
    )
    seats_wanted = fields.Integer(
        readonly=True,
        related="opportunity_id.seats_wanted",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        domain="""
            [
                ("sale_ok", "=", True),
                ("event_reservation_type_id", "=", event_type_id),
            ]
        """,
        context="""
            {
                "default_event_reservation_ok": True,
                "default_event_reservation_type_id": event_type_id,
            }
        """,
        index=True,
        ondelete="cascade",
        string="Product",
    )
    event_id = fields.Many2one(
        comodel_name="event.event",
        domain="""
            [
                ("event_type_id", "=", event_type_id),
                ("date_end", ">=", datetime.date.today().strftime("%Y-%m-%d")),
                ("is_finished", "!=", True),
                "|",
                ("seats_limited", "=", "False"),
                ("seats_available", ">=", seats_wanted),
            ]
        """,
        context="""
            {
                "default_event_type_id": event_type_id,
            }
        """,
        index=True,
        ondelete="cascade",
        string="Event",
    )
    event_ticket_id = fields.Many2one(
        comodel_name="event.event.ticket",
        domain="""
            [
                ("event_id", "=", event_id),
                "|",
                ("end_sale_datetime", "=", False),
                ("end_sale_datetime", ">=", datetime.date.today().strftime("%Y-%m-%d")),
                "|",
                ("seats_limited", "=", "False"),
                ("seats_available", ">=", seats_wanted),
            ]
        """,
        context="""
            {
                "default_event_id": event_id,
            }
        """,
        index=True,
        ondelete="cascade",
        string="Ticket",
    )

    def action_generate(self):
        """Create an event reservation sales order."""
        # Creating a sale order properly involves lots of onchanges, so here it
        # is better to use `Form` to make sure we forget none
        so_form = Form(self.env["sale.order"])
        so_form.campaign_id = self.opportunity_id.campaign_id
        so_form.medium_id = self.opportunity_id.medium_id
        so_form.opportunity_id = self.opportunity_id
        so_form.origin = self.opportunity_id.name
        so_form.partner_id = self.opportunity_id.partner_id
        so_form.source_id = self.opportunity_id.source_id
        so_form.team_id = self.opportunity_id.team_id
        with so_form.order_line.new() as so_line:
            if self.mode == "reserve":
                assert self.product_id
                so_line.product_id = self.product_id
                so_line.product_uom_qty = self.opportunity_id.seats_wanted
            elif self.mode == "register":
                assert self.event_id
                assert self.event_ticket_id
                so_line.product_id = self.event_ticket_id.product_id
                so_line.product_uom_qty = self.opportunity_id.seats_wanted
                so_line.event_id = self.event_id
                so_line.event_ticket_id = self.event_ticket_id
        so = so_form.save()
        return {
            "res_id": so.id,
            "res_model": "sale.order",
            "type": "ir.actions.act_window",
            "view_mode": "form",
        }
