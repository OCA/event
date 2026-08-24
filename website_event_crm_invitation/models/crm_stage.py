# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CRMStage(models.Model):
    _inherit = "crm.stage"

    auto_advance_stage_invite_website_event_type = fields.Boolean(
        string="Advance stage automatically when inviting to website event category",
        help=(
            "When an opportunity in this stage is invited to a website "
            "event category, it will advance automatically to the next stage."
        ),
    )
    auto_invite_website_event_type = fields.Boolean(
        string="Invite automatically to website event category",
        help=(
            "When an opportunity is in this stage and there is any new event "
            "published for its category with available seats, opportunities "
            "found in this stage will get invited to it and moved to the "
            "next stage automatically."
        ),
    )
