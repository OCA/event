# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventMailConfigSettings(models.TransientModel):
    _inherit = 'event.config.settings'

    event_mail_template_id = fields.Many2one(
        comodel_name='event.mail.template',
        string='Mail Template',
    )

    @api.multi
    def set_default_event_mail_template_id(self):
        self.env['ir.values'].set_default(
            'event.config.settings', 'event_mail_template_id',
            self.event_mail_template_id.id)
