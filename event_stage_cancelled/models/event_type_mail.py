# Copyright 2024 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventTypeMail(models.Model):
    _inherit = "event.type.mail"

    interval_type = fields.Selection(
        selection_add=[("after_cancel", "After the event cancellation")],
        ondelete={"after_cancel": "cascade"},
    )
