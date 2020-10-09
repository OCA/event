# Copyright 2019 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    website_require_login = fields.Boolean(
        string="Require login for website registrations",
        help="If set, a user must be logged in to be able to register "
        "attendees from the website.",
    )
