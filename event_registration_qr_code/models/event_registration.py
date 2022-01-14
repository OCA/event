# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import uuid

from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    qr_code = fields.Char(
        compute="_compute_qr_code",
        store=True,
        index=True,
        copy=False,
    )

    _sql_constraints = [
        ("qr_code_unique", "unique(qr_code)", "QR Code should be unique")
    ]

    @api.depends("event_id")
    def _compute_qr_code(self):
        for rec in self:
            if not rec.qr_code:
                rec.qr_code = uuid.uuid4().hex
