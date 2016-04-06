# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    contact_ids = fields.Many2many(
        string='Contacts',
        comodel_name='res.partner',
        help='Partners available to attend attendees requests for this event.')

    @api.multi
    @api.onchange("type")
    def _onchange_type_set_contact_ids(self):
        if self.type.contact_ids and not self.contact_ids:
            self.contact_ids = self.type.contact_ids


class EventType(models.Model):
    _inherit = 'event.type'

    contact_ids = fields.Many2many(
        string='Contacts',
        comodel_name='res.partner',
        help='Partners available to attend attendees requests by default for '
             'events of this type.')
