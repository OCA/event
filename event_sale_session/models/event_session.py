# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventSession(models.Model):
    _inherit = "event.session"

    # NOTE: This field name doesn't follow the convention but it's kept like this
    #       to match the field name in core `event.event` model.
    sale_order_lines_ids = fields.One2many(
        comodel_name="sale.order.line",
        inverse_name="event_session_id",
        groups="sales_team.group_sale_salesman",
        string="All sale order lines pointing to this session",
    )
    sale_price_subtotal = fields.Monetary(
        string="Sales (Tax Excluded)",
        compute="_compute_sale_price_subtotal",
        groups="sales_team.group_sale_salesman",
    )

    @api.depends(
        "currency_id",
        "sale_order_lines_ids.price_subtotal",
        "sale_order_lines_ids.currency_id",
        "sale_order_lines_ids.company_id",
        "sale_order_lines_ids.order_id.date_order",
    )
    def _compute_sale_price_subtotal(self):
        """Compute Sales (Tax Excluded)

        This method is almost exactly the same than the one in core event_sale module
        :meth:`~event_sale.models.event_event._compute_sale_price_subtotal`, only here
        we compute the event.session data instead.
        """
        date_now = fields.Datetime.now()
        sale_price_by_session = {}
        if self.ids:
            session_subtotals = self.env["sale.order.line"].read_group(
                [
                    ("state", "!=", "cancel"),
                    ("event_session_id", "in", self.ids),
                    ("price_subtotal", "!=", 0),
                ],
                ["event_session_id", "currency_id", "price_subtotal:sum"],
                ["event_session_id", "currency_id"],
                lazy=False,
            )
            currency_ids = [
                session_subtotal["currency_id"][0]
                for session_subtotal in session_subtotals
            ]
            company_by_session = {
                rec._origin.id or rec.id: rec.company_id for rec in self
            }
            currency_by_session = {
                rec._origin.id or rec.id: rec.currency_id for rec in self
            }
            currency_by_id = {
                currency.id: currency
                for currency in self.env["res.currency"].browse(currency_ids)
            }
            for session_subtotal in session_subtotals:
                price_subtotal = session_subtotal["price_subtotal"]
                session_id = session_subtotal["event_session_id"][0]
                currency_id = session_subtotal["currency_id"][0]
                sale_price = currency_by_session[session_id]._convert(
                    price_subtotal,
                    currency_by_id[currency_id],
                    company_by_session[session_id],
                    date_now,
                )
                if session_id in sale_price_by_session:
                    sale_price_by_session[session_id] += sale_price
                else:
                    sale_price_by_session[session_id] = sale_price

        for rec in self:
            rec.sale_price_subtotal = sale_price_by_session.get(
                rec._origin.id or rec.id, 0
            )

    def action_view_linked_orders(self):
        """View sales orders

        Simlar to :meth:`~event_sale.models.event_event.action_view_linked_orders`
        """
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_orders")
        action["domain"] = [
            ("state", "!=", "cancel"),
            ("order_line.event_session_id", "in", self.ids),
        ]
        return action
