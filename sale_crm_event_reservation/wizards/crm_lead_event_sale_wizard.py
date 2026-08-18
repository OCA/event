# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, api, fields, models


class CRMLeadEventSale(models.TransientModel):
    _name = "crm.lead.event.sale.wizard"
    _description = "Wizard to generate event quotation from event opportunity"

    opportunity_id = fields.Many2one(
        comodel_name="crm.lead",
        index=True,
        ondelete="cascade",
        readonly=True,
        required=True,
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
        index=True,
        ondelete="cascade",
    )
    allowed_event_ids = fields.Many2many(
        comodel_name="event.event",
        compute="_compute_allowed_event_ids",
        readonly=True,
    )
    event_id = fields.Many2one(
        comodel_name="event.event",
        domain="[('id', 'in', allowed_event_ids)]",
        index=True,
        ondelete="cascade",
    )
    allowed_event_ticket_ids = fields.Many2many(
        comodel_name="event.event.ticket",
        compute="_compute_allowed_event_ticket_ids",
        readonly=True,
    )
    event_ticket_id = fields.Many2one(
        comodel_name="event.event.ticket",
        domain="[('id', 'in', allowed_event_ticket_ids)]",
        index=True,
        ondelete="cascade",
        string="Ticket",
    )

    @api.depends("mode")
    def _compute_allowed_event_ids(self):
        for record in self:
            events = self.env["event.event"].search(
                [
                    ("event_type_id", "=", record.event_type_id.id),
                    ("date_end", ">=", fields.Date.context_today(self)),
                    ("is_finished", "=", False),
                ]
            )
            record.allowed_event_ids = events.filtered(
                lambda event: not event.seats_limited
                or event.seats_available >= self.seats_wanted
            )

    @api.depends("event_id")
    def _compute_allowed_event_ticket_ids(self):
        for record in self:
            record.allowed_event_ticket_ids = []
            if record.event_id:
                tickets = record.event_id.event_ticket_ids.filtered(
                    lambda ticket, record=record: (
                        not ticket.end_sale_datetime
                        or ticket.end_sale_datetime >= fields.Datetime.now()
                    )
                    and (
                        not ticket.seats_limited
                        or ticket.seats_available >= record.seats_wanted
                    )
                )
                record.allowed_event_ticket_ids = tickets

    def action_generate(self):
        """Create an event reservation sales order."""
        so_vals = {
            "partner_id": self.opportunity_id.partner_id.id,
            "campaign_id": self.opportunity_id.campaign_id.id,
            "medium_id": self.opportunity_id.medium_id.id,
            "opportunity_id": self.opportunity_id.id,
            "origin": self.opportunity_id.name,
            "source_id": self.opportunity_id.source_id.id,
            "team_id": self.opportunity_id.team_id.id,
        }
        if self.mode == "reserve":
            assert self.product_id
            so_line_vals = {
                "product_id": self.product_id.id,
                "product_uom_qty": self.opportunity_id.seats_wanted,
            }
        elif self.mode == "register":
            assert self.event_id
            assert self.event_ticket_id
            so_line_vals = {
                "product_id": self.event_ticket_id.product_id.id,
                "product_uom_qty": self.opportunity_id.seats_wanted,
                "event_id": self.event_id.id,
                "event_ticket_id": self.event_ticket_id.id,
            }
        so_vals["order_line"] = [Command.create(so_line_vals)]
        so = self.env["sale.order"].create(so_vals)
        return {
            "res_id": so.id,
            "res_model": "sale.order",
            "type": "ir.actions.act_window",
            "view_mode": "form",
        }
