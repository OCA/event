# Copyright 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    event_mail_template_id = fields.Many2one(
        comodel_name='event.mail',
        string='Mail Template',
    )

    @api.multi
    def set_default_event_mail_template_id(self):
        self.env['ir.default'].set(
            'res.config.settings', 'event_mail_template_id',
            self.event_mail_template_id.id
        )
