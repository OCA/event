# Copyright 2023 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class Event(models.Model):
    _inherit = "event.event"

    unique_attendee_email = fields.Boolean(
        string="Unique registration email", default=False
    )
    email_duplication_behaviour = fields.Selection(
        selection=[
            ("update", "Delete and recreate registration"),
            ("ignore", "Ignore new registration"),
        ],
        string="Duplicated email registration behaviour",
    )
