# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventMailConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    event_mail_template_id = fields.Many2one(
        comodel_name='event.mail.template',
        string='Mail Template',
    )

    auto_confirmation = fields.Selection([
        (1, 'No validation step on registration'),
        (0, "Manually confirm every registration")
        ], "Auto Confirmation",
        help='Unselect this option to manually'
        'manage draft event and draft registration')

    @api.multi
    def set_values(self):
        self.env['ir.default'].set(
            'res.config.settings', 'event_mail_template_id',
            self.event_mail_template_id.id)
