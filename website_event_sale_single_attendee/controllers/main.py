# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import http
from odoo.http import request

from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController


class WebsiteEventSaleControllerSingleAttendee(WebsiteEventSaleController):
    def _process_attendees_form(self, event, form_details):
        """Multiply single attendee registration according to ticket qties"""
        registrations = super()._process_attendees_form(event, form_details)
        if len(registrations) == 1 and "event_ticket_id" not in registrations[0]:
            # Get the quantities for each ticket_id
            ticket_ids_quantities = {}
            for key, value in form_details.items():
                if key.startswith("ticket_id_qty-"):
                    ticket_id = key.split("-", 1)[1]
                    ticket_ids_quantities[ticket_id] = value

            # Multiply registration details for each ticket according to the
            # quantities
            if ticket_ids_quantities:
                registration_details = registrations[0]
                registrations = []
                for ticket_id, qty in ticket_ids_quantities.items():
                    for _ in range(int(qty)):
                        reg = registration_details.copy()
                        reg["event_ticket_id"] = int(ticket_id) or False
                        registrations.append(reg)
        return registrations

    @http.route(
        ['/event/<model("event.event"):event>/registration/new'],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def registration_new(self, event, **post):
        if not event.single_attendee_registration:
            return super().registration_new(event, **post)
        # Reimplementation of super method with change of rendered template
        tickets = self._process_tickets_form(event, post)
        availability_check = True
        if event.seats_limited:
            ordered_seats = 0
            for ticket in tickets:
                ordered_seats += ticket["quantity"]
            if event.seats_available < ordered_seats:
                availability_check = False
        if not tickets:
            return False
        default_first_attendee = {}
        if not request.env.user._is_public():
            default_first_attendee = {
                "name": request.env.user.name,
                "email": request.env.user.email,
                "phone": request.env.user.mobile or request.env.user.phone,
            }
        else:
            visitor = request.env["website.visitor"]._get_visitor_from_request()
            if visitor.email:
                default_first_attendee = {
                    "name": visitor.name,
                    "email": visitor.email,
                    "phone": visitor.mobile,
                }
        return request.env["ir.ui.view"]._render_template(
            "website_event_sale_single_attendee.registration_attendee_details_single",
            {
                "tickets": tickets,
                "event": event,
                "availability_check": availability_check,
                "default_first_attendee": default_first_attendee,
            },
        )
