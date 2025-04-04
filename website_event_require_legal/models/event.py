# Copyright 2025 Tecnativa - Pilar Vargas
# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    website_require_legal = fields.Boolean(
        string="Require legal terms",
        help="If set, the user must accept the terms in order to register in the event "
        "from the website.",
    )
    website_description_legal = fields.Html(
        string="Legal Terms Description",
        help="Custom text for the legal terms checkbox shown on the event "
        "registration page. Leave empty to use the default text.",
        translate=True,
    )
