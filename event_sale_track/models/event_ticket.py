# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventTicket(models.Model):
    _inherit = 'event.event.ticket'

    track_id = fields.Many2one(
        'event.track',
        string='Track',
    )
    event_id = fields.Many2one(
        'event.event',
        related='track_id.event_id',
        store=True
    )
    # `event_sale` has this relation as o2m.
    # Registrations can be subscribed to different tracks/tickets now.
    # TODO: any particular pre/post/uninstal hook
    # to consider for smooth transition?
    registration_ids = fields.Many2many(
        comodel_name='event.registration',
        relation='event_ticket_registration_rel',
        column1='ticket_id',
        column2='registration_id',
        string='Registrations',
    )

    @api.multi
    @api.depends('seats_max', 'registration_ids.state')
    def _compute_seats(self):
        """Overridden to consider only attendees relate to current tickets.

        This method is mostly the same but the query is different.
        We want to select only attendees matching tickets
        via `event_ticket_registration_rel`.
        """
        # initialize fields to 0 + compute seats availability
        browse_map = {}
        for ticket in self:
            # TODO: not sure this has any effect as record should be cached
            # already when `self.browse` below is called
            browse_map[ticket.id] = ticket
            ticket.update({
                'seats_availability':
                    'unlimited' if ticket.seats_max == 0 else 'limited',
                'seats_unconfirmed': 0,
                'seats_reserved': 0,
                'seats_used': 0,
                'seats_available': 0,
            })
        # aggregate registrations by ticket and by state
        if self.ids:
            state_field = {
                'draft': 'seats_unconfirmed',
                'open': 'seats_reserved',
                'done': 'seats_used',
            }
            raw_data = self._get_compute_seats_raw_data(self.ids)
            for event_ticket_id, state, num in raw_data:
                ticket = browse_map[event_ticket_id]
                ticket[state_field[state]] += num

        # compute seats_available
        for ticket in self:
            if ticket.seats_max > 0:
                ticket.seats_available = ticket.seats_max - (
                    ticket.seats_reserved + ticket.seats_used)

    def _get_compute_seats_raw_data(self, ticket_ids):
        query = """
            SELECT
                rel.ticket_id, reg.state, count(event_id)
            FROM
                event_ticket_registration_rel rel, event_registration reg
            WHERE
                rel.ticket_id IN  %s
                AND reg.id = rel.registration_id
                AND reg.state IN ('draft', 'open', 'done')
            GROUP BY rel.ticket_id, reg.state
        """
        self.env.cr.execute(query, (tuple(ticket_ids),))
        return self.env.cr.fetchall()
