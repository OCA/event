# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    registration_ids = fields.One2many(
        comodel_name="event.registration",
        inverse_name="sale_order_id",
        string="Attendees",
        readonly=True,
    )
    event_ids = fields.Many2many(
        comodel_name="event.event",
        string="Event",
        compute="_compute_event_ids",
        readonly=True,
    )

    @api.depends("order_line.event_id")
    def _compute_event_ids(self):
        for sale in self:
            sale.event_ids = sale.order_line.event_id

    def _session_seats_available(self):
        """Check if there are lines that could do session overbooking"""
        sessions = {}
        for line in self.mapped("order_line").filtered("event_session_seats_limited"):
            sessions.setdefault(line.session_id, line.event_session_seats_available)
            sessions[line.session_id] -= line.product_uom_qty
            # Break if any session can't allocate seats
            if sessions[line.session_id] < 0:
                return False
        return True


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    session_id = fields.Many2one(comodel_name="event.session", string="Session")
    event_sessions_count = fields.Integer(
        comodel_name="event.session",
        related="event_id.sessions_count",
        readonly=True,
    )
    event_session_seats_available = fields.Integer(
        related="session_id.seats_available",
        string="Available Seats",
        readonly=True,
    )
    event_session_seats_limited = fields.Boolean(
        related="session_id.seats_limited",
        string="Seats Availavility",
        readonly=True,
    )
    registration_ids = fields.One2many(
        comodel_name="event.registration",
        inverse_name="sale_order_line_id",
        string="Attendees",
        readonly=True,
    )

    @api.onchange("session_id")
    def onchange_session_id(self):
        """Don't allow to book seats if there aren't enough"""
        if not self.order_id._session_seats_available():
            raise ValidationError(_("Not enough seats. Change quantity or session"))

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        """Don't allow to book seats if there aren't enough"""
        if not self.order_id._session_seats_available():
            raise ValidationError(_("Not enough seats. Change quantity or session"))
        return super().product_uom_change()

    @api.onchange("event_id")
    def _onchange_event_id(self):
        """Force default session"""
        if self.event_sessions_count == 1:
            self.session_id = self.event_id.session_ids[0]
        return super()._onchange_event_id()

    def get_sale_order_line_multiline_description_sale(self, product):
        """Add the session name"""
        name = super().get_sale_order_line_multiline_description_sale(product)
        if self.event_ticket_id and self.session_id:
            name += "\n" + self.session_id.display_name
        return name
