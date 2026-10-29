# Copyright 2019 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    event_mail_template_id = fields.Many2one(
        comodel_name="event.mail.template",
        string="Mail Template",
    )
