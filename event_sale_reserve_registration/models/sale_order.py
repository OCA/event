# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def do_registrations(self):
        for order in self:
            order.order_line._update_registrations(
                confirm=False, cancel_to_draft=False, registration_data=None
            )

        return True

    def confirm_reserved_registrations(self):
        for sale in self:
            sale.order_line._update_registrations(confirm=True, cancel_to_draft=False)

    @api.depends("event_registration_ids")
    def _compute_attendee_count(self):
        for rec in self:
            rec.attendees_count = len(rec.event_registration_ids)

    event_registration_ids = fields.One2many(
        "event.registration", "sale_order_id", string="Attendee list"
    )
    attendees_count = fields.Integer(compute="_compute_attendee_count")

    def action_view_attendees(self):
        registrations = self.mapped("event_registration_ids")
        action = self.env.ref("event.action_registration").read()[0]
        if len(registrations) > 1:
            action["domain"] = [("id", "in", registrations.ids)]
        elif len(registrations) == 1:
            form_view = [(self.env.ref("account.view_move_form").id, "form")]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = registrations.id
        else:
            action = {"type": "ir.actions.act_window_close"}

        return action
