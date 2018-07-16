# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2016 Jamotion

from openerp import models, api


class EventEventTicket(models.Model):
    _inherit = 'event.event.ticket'

    @api.multi
    def get_seats_range(self):
        self.ensure_one()
        min_seats = self.event_id.registration_seats_min
        max_seats = min(min(
            self.event_id.registration_seats_max or 9,
            self.seats_available or 9) + 1, 10)
        return range(min_seats, max_seats)
