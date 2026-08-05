# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import http

from odoo.addons.website_event_sale.controllers import main as website_event_sale_main


class WebsiteEventController(website_event_sale_main.WebsiteEventSaleController):
    def _process_attendees_form(self, event, form_details):
        registration_data = super()._process_attendees_form(event, form_details)
        for registration_vals in registration_data:
            ticket_id = registration_vals.get("event_ticket_id")
            multi_qty = form_details.get(f"use_multi_qty-{ticket_id or 0}")
            if multi_qty:
                registration_vals["qty"] = int(multi_qty)
        return registration_data

    def _create_attendees_from_registration_post(self, event, registration_data):
        ticket2qty = {
            registration_vals["event_ticket_id"]: registration_vals["qty"]
            for registration_vals in registration_data
            if registration_vals.get("qty") and registration_vals.get("event_ticket_id")
        }
        http.request.update_context(multi_qty_disable_sync=True)
        registrations = super()._create_attendees_from_registration_post(
            event, registration_data
        )
        order = http.request.website.sale_get_order()
        for ticket_id, qty in ticket2qty.items():
            ticket = http.request.env["event.event.ticket"].sudo().browse(ticket_id)
            order._cart_update(
                product_id=ticket.product_id.id,
                event_ticket_id=ticket_id,
                add_qty=qty - 1,
            )
        http.request.session["website_sale_cart_quantity"] = order.cart_quantity
        return registrations
