# Copyright 2024 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventStage(models.Model):
    _inherit = "event.stage"

    is_cancelled = fields.Boolean(help="The event is cancelled")
