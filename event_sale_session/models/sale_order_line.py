# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    event_use_sessions = fields.Boolean(related="event_id.use_sessions")
    event_session_id = fields.Many2one(
        string="Session",
        comodel_name="event.session",
        domain="[('event_id', '=', event_id)]",
    )

    @api.onchange("event_id")
    def _onchange_event_id(self):
        # OVERRIDE to automatically set the session, if there's only one available
        # and also to clear event_session_id if it's inconsistent with the event
        event = self.event_id
        if event.session_count == 1:
            self.event_session_id = event.session_ids[0]
        elif not event.use_sessions or event != self.event_session_id.event_id:
            self.event_session_id = False
        return super()._onchange_event_id()

    @api.onchange("event_session_id")
    def _onchange_event_session_id(self):
        # We call this to force update the default name
        # Simliar to :meth:`~_onchange_event_ticket_id` in core.
        self.product_id_change()

    def get_sale_order_line_multiline_description_sale(self, product):
        res = super().get_sale_order_line_multiline_description_sale(product)
        if self.event_session_id:
            lang = self.order_id.partner_id.lang
            session = self.event_session_id.with_context(lang=lang)
            res += "\n" + session.with_context(with_event_name=False).display_name
        return res
