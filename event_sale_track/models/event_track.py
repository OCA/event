# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class Track(models.Model):
    _inherit = 'event.track'

    ticket_ids = fields.One2many(
        comodel_name='event.event.ticket',
        inverse_name='track_id',
        string='Tickets'
    )
    seats_max = fields.Integer(
        string='Maximum Available Seats',
        compute='_compute_seats',
    )
    seats_reserved = fields.Integer(
        string='Reserved Seats',
        compute='_compute_seats',
        store=True,
    )
    seats_available = fields.Integer(
        string='Available Seats',
        compute='_compute_seats',
        store=True
    )
    seats_unconfirmed = fields.Integer(
        string='Unconfirmed Seat Reservations',
        compute='_compute_seats',
        store=True
    )
    seats_used = fields.Integer(compute='_compute_seats', store=True)

    @api.multi
    @api.depends(
        'ticket_ids.seats_max',
        'ticket_ids.seats_unconfirmed',
        'ticket_ids.seats_available',
        'ticket_ids.seats_reserved',
        'ticket_ids.seats_used',
    )
    def _compute_seats(self):
        """Compute seats based on tickets counters."""
        counters = (
            'seats_max', 'seats_unconfirmed',
            'seats_available', 'seats_reserved',
            'seats_used',
        )
        for item in self:
            vals = {}
            for fname in counters:
                vals[fname] = sum(item.ticket_ids.mapped(fname))
            item.update(vals)
