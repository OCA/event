# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class Attendee(models.Model):
    _inherit = 'event.registration'

    # TODO: prevent same attendee to be subscribed 2 times
    # to the same track w/ a different ticket
    ticket_ids = fields.Many2many(
        comodel_name='event.event.ticket',
        column1='registration_id',
        column2='ticket_id',
        relation='event_ticket_registration_rel',
        string='Tickets'
    )
    track_ids = fields.Many2many(
        comodel_name='event.track',
        compute='_compute_track_ids',
    )

    @api.multi
    @api.depends('ticket_ids')
    def _compute_track_ids(self):
        for rec in self:
            rec.track_ids = rec.mapped('ticket_ids.track_id')

    @api.model
    def create(self, vals):
        """Reflect `event_ticket_id` on `ticket_ids`."""
        if vals.get('event_ticket_id') and not vals.get('ticket_ids'):
            vals['ticket_ids'] = [(4, vals['event_ticket_id'])]
        rec = super().create(vals)
        return rec

    @api.multi
    def write(self, vals):
        """Reflect `event_ticket_id` on `ticket_ids`."""
        res = super().write(vals)
        for rec in self:
            if not rec.event_ticket_id:
                continue
            if rec.event_ticket_id not in rec.ticket_ids:
                rec.ticket_ids += rec.event_ticket_id
        return res
