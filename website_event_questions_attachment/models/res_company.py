# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    max_attachment_size = fields.Integer(
        default=0,
        help="Maximum file size in MB for event registration attachments.\
        0 = no limit.",
    )
