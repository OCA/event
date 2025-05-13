# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventStage(models.Model):
    _inherit = "event.stage"

    exclude_from_email_reminder = fields.Boolean(string="Exclude from email reminder")
