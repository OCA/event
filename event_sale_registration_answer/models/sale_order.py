# Copyright (C) 2024 Open Source Integrators (https://www.opensourceintegrators.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    registration_ids = fields.One2many("event.registration", "sale_order_id")

    def action_view_questions_list(self):
        list_view = self.env.ref(
            "event_sale_registration_answer.event_registration_answer_view_tree_so"
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Questions"),
            "res_model": "event.registration.answer",
            "view_type": "list",
            "view_mode": "list",
            "views": [(list_view.id, "list")],
            "domain": [("registration_id.sale_order_id", "=", self.id)],
            "context": {"search_default_group_by_registration": 1},
        }

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        # Allow disable automatic populate answer for some specific use cases
        # by seeting a special special key in the Context
        if not self.env.context.get("skip_action_confirm_populate_answers"):
            self.registration_ids.populate_answers()
        return res
