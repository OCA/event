# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo import exceptions


class SaleOrder(models.Model):
    _inherit = "sale.order"

    registration_ids = fields.One2many(
        comodel_name='event.registration',
        inverse_name='sale_order_id',
        string='Attendees',
        readonly=True,
    )
    event_ids = fields.Many2many(
        comodel_name="event.event",
        string='Event',
        compute='_compute_event_ids',
        readonly=True,
    )

    @api.multi
    @api.depends('order_line.event_id')
    def _compute_event_ids(self):
        for sale in self:
            sale.event_ids = sale.order_line.mapped('event_id')

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
    )
    event_sessions_count = fields.Integer(
        comodel_name='event.session',
        related='event_id.sessions_count',
        readonly=True,
    )
    event_session_seats_available = fields.Integer(
        related='session_id.seats_available',
        string='Available Seats',
        readonly=True,
    )
    event_session_seats_availability = fields.Selection(
        related='session_id.seats_availability',
        string='Seats Availavility',
        readonly=True,
    )
    registration_ids = fields.One2many(
        comodel_name='event.registration',
        inverse_name='sale_order_line_id',
        string='Attendees',
        readonly=True,
    )

    @api.multi
    def write(self, values):
        super(SaleOrderLine, self).write(values)
        for line in self:
            if not line._session_seats_available():
                raise exceptions.ValidationError(_(
                    "There are sessions with no available seats!\n"
                    "Edit them so you can save the sale order"))

    @api.onchange(
        'product_uom_qty', 'event_id', 'session_id', 'event_ticket_id')
    def product_uom_change(self):
        super(SaleOrderLine, self).product_uom_change()
        if self.session_id:
            if not self._session_seats_available():
                raise exceptions.UserError(_(
                    "Not enough seats. Change quanty or session"))

    @api.multi
    @api.onchange('event_id', 'session_id', 'event_ticket_id')
    def event_id_change(self):
        for so_line in self:
            so_line.name = so_line._set_order_line_description()
            if self.event_sessions_count == 1:
                so_line.session_id = self.event_id.session_ids[0]

    def _session_seats_available(self):
        self.ensure_one()
        if self.session_id and self.session_id.seats_availability == 'limited':
            seats = self.event_session_seats_available - self.product_uom_qty
            return True if seats > 0 else False
        else:
            return True

    def _set_order_line_description(self):
        description = self.event_id.name or self.product_id.name
        if self.session_id:
            description += ' - %s' % self.session_id.name or ''
        if self.event_ticket_id:
            description += ' - %s' % self.event_ticket_id.name or ''
        return description
