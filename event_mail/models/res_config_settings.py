# Copyright 2016 Tecnativa - Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    event_mail_template_id = fields.Many2one(
        related="company_id.event_mail_template_id",
        comodel_name="event.mail.template",
        string="Mail Template",
        readonly=False,
    )
