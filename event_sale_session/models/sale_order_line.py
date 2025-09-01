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
        compute="_compute_event_session_id",
        domain="[('event_id', '=', event_id)]",
        store=True,
        readonly=False,
        precompute=True,
    )

    @api.depends("event_id")
    def _compute_event_session_id(self):
        event_lines = self.filtered("event_id")
        (self - event_lines).event_session_id = False
        for line in event_lines:
            if (
                not line.event_id.use_sessions
                or line.event_id != line.event_session_id.event_id
            ):
                line.event_session_id = False
            if line.event_id.session_count == 1:
                line.event_session_id = line.event_id.session_ids[0]

    @api.depends("event_session_id")
    def _compute_name(self):
        # OVERRIDE to add the compute method dependency.
        #
        # Simliar to what's done in core for the `event_ticket_id` field.
        # See :meth:`~_get_sale_order_line_multiline_description_sale`
        return super()._compute_name()

    def _get_sale_order_line_multiline_description_sale(self):
        res = super()._get_sale_order_line_multiline_description_sale()
        if self.event_session_id:
            lang = self.order_id.partner_id.lang
            session = self.event_session_id.with_context(lang=lang)
            res += "\n" + session.with_context(with_event_name=False).display_name
        return res
