# -*- coding: utf-8 -*-
# Copyright 2017,2018 IT-Projects LLC - Ivan Yelizariev
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models, fields, api


class EventRegistration(models.Model):

    _inherit = 'event.registration'

    event_ticket_price = fields.Float(
        related='event_ticket_id.price',
        readonly=True)
    user_is_manager = fields.Boolean(compute='_compute_user_is_manager')

    @api.multi
    def _compute_user_is_manager(self):
        user_is_manager = self.env.user.has_group('event.group_event_manager')
        for r in self:
            r.user_is_manager = user_is_manager
