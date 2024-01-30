# Copyright (C) 2024 Open Source Integrators (https://www.opensourceintegrators.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_view_questions_list(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Questions"),
            "res_model": "event.registration.answer",
            "view_type": "list",
            "view_mode": "list",
            "views": [
                (
                    self.env.ref(
                        "event_sale_registration_answer."
                        "event_registration_answer_view_tree_so"
                    ).id,
                    "list",
                )
            ],
            "domain": [("registration_id.sale_order_id", "=", self.id)],
            "context": {"search_default_group_by_registration": 1},
        }

    def _prepare_event_reg_answer_vals(self, registration, question):
        answer_vals = {
            "question_id": question.id,
            "registration_id": registration.id,
            "partner_id": registration.partner_id.id,
            "event_id": registration.event_id.id,
            "question_type": question.question_type,
        }
        return answer_vals

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            if so.attendee_count > 0:
                event_reg_answer_obj = self.env["event.registration.answer"]
                event_reg_recs = self.env["event.registration"].search(
                    [("sale_order_id", "=", so.id), ("state", "!=", "cancel")],
                    order="id asc",
                )
                for registration in event_reg_recs:
                    questions = registration.event_id.question_ids
                    for question in questions:
                        if question.once_per_order:
                            event_reg_answer_rec = event_reg_answer_obj.search(
                                [
                                    ("question_id", "=", question.id),
                                    ("registration_id", "=", event_reg_recs[0].id),
                                ]
                            )
                            if event_reg_answer_rec:
                                continue
                            answer_vals = self._prepare_event_reg_answer_vals(
                                event_reg_recs[0], question
                            )
                        else:
                            answer_vals = self._prepare_event_reg_answer_vals(
                                registration, question
                            )
                        event_reg_answer_obj.create(answer_vals)
        return res
