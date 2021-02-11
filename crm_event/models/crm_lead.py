# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    event_type_id = fields.Many2one(
        comodel_name="event.type",
        index=True,
        ondelete="restrict",
        string="Event category",
        help=(
            "If this lead/opportunity is related to a specific event category, "
            "indicate it here."
        ),
    )
    seats_wanted = fields.Integer(
        groups="event.group_event_user",
        help=(
            "If this lead/opportunity is related to a specific event category, "
            "indicate how many seats would you sell if won."
        ),
    )
