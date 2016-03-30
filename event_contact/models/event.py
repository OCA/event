# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class event_event(models.Model):
    _inherit = 'event.event'

    contact_ids = fields.Many2many(
        string='Contacts',
        comodel_name='res.partner')
