import logging

from odoo import _, http
from odoo.http import request

import odoo.addons.website_sale.controllers.main as website_sale

_logger = logging.getLogger(__name__)


class WebsiteSale(website_sale.WebsiteSale):
    @http.route(
        ["/shop/check_before_payment"], type="json", auth="public", website=True
    )
    def check_before_payment(self):
        order = request.website.sale_get_order()
        if order:
            if order.state == "cancel":
                return {
                    "valid": False,
                    "message": request.env.company.cancelled_order_message,
                }

            order_lines_by_event = (
                request.env["sale.order.line"]
                .sudo()
                .read_group(
                    [("order_id", "=", order.id)], ["product_uom_qty"], ["event_id"]
                )
            )
            for lines_group in order_lines_by_event:
                event = request.env["event.event"].browse(lines_group["event_id"][0])
                if not self._check_event_availability(
                    event, lines_group["product_uom_qty"]
                ):
                    self._cancel_cart_with_unavailable_seats(order)
                    return {
                        "valid": False,
                        "message": (request.env.company.no_more_seats_on_event_message),
                    }

            order_lines_by_ticket = (
                request.env["sale.order.line"]
                .sudo()
                .read_group(
                    [("order_id", "=", order.id)],
                    ["product_uom_qty"],
                    ["event_ticket_id"],
                )
            )
            for lines_group in order_lines_by_ticket:
                ticket = request.env["event.event.ticket"].browse(
                    lines_group["event_ticket_id"][0]
                )
                if not self._check_ticket_availability(
                    ticket, lines_group["product_uom_qty"]
                ):
                    self._cancel_cart_with_unavailable_seats(order)
                    return {
                        "valid": False,
                        "message": request.env.company.no_more_ticket_message,
                    }
        return {"valid": True}

    def _check_event_availability(self, event, ticket_qty):
        if event.seats_availability == "limited":
            if event.seats_available < ticket_qty:
                return False
        return True

    def _check_ticket_availability(self, ticket, ticket_qty):
        if ticket.seats_availability == "limited":
            if ticket.seats_available < ticket_qty:
                return False
        return True

    def _cancel_cart_with_unavailable_seats(self, cart):
        cart.action_cancel()
        cart.message_post(body=_("Seats not available anymore"))
