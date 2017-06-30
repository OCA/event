# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    contact_ids = fields.Many2many(
        string='Contacts',
        comodel_name='res.partner',
        help='Partners available to attend attendees requests for this event.')

    @api.onchange("event_type_id")
    def _onchange_type_set_contact_ids(self):
        self.contact_ids |= self.event_type_id.contact_ids
