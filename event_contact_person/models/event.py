# -*- coding: utf-8 -*-
# © 2016 Michael Viriyananda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class event_event(models.Model):
    _inherit = 'event.event'

    contact_person_ids = fields.Many2many(
        string='Contact Persons',
        comodel_name='res.partner',
        relation='event_contact_person_rel',
        column1='event_id',
        column2='partner_id')
