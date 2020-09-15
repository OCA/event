# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import http
from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController
from odoo.http import request


class WebsiteEventSaleControllerSingleAttendee(WebsiteEventSaleController):

    def _process_registration_details(self, details):
        """Multiply single attendee registration according to ticket qties"""
        registrations = super()._process_registration_details(details)
        if len(registrations) == 1 and "ticket_id" not in registrations[0]:
            # Get the quantities for each ticket_id
            registration_details = {}
            ticket_ids_quantities = {}
            for key, value in registrations[0].items():
                if key.startswith("ticket_id_qty-"):
                    ticket_id = key.split("-", 1)[1]
                    ticket_ids_quantities[ticket_id] = value
                else:
                    registration_details[key] = value
            # Multiply registration details for each ticket according to the
            # quantities
            if ticket_ids_quantities:
                registrations = []
                for ticket_id, qty in ticket_ids_quantities.items():
                    for cnt in range(0, int(qty)):
                        reg = registration_details.copy()
                        reg["ticket_id"] = ticket_id
                        registrations.append(reg)
        return registrations

    @http.route(['/event/<model("event.event"):event>/registration/new'],
                type='json', auth="public", methods=['POST'], website=True)
    def registration_new(self, event, **post):
        if not event.single_attendee_registration:
            return super().registration_new(event, **post)
        # Reimplementation of super method with change of rendered template
        tickets = self._process_tickets_details(post)
        availability_check = True
        if event.seats_availability == 'limited':
            ordered_seats = 0
            for ticket in tickets:
                ordered_seats += ticket['quantity']
            if event.seats_available < ordered_seats:
                availability_check = False
        if not tickets:
            return False
        return request.env['ir.ui.view'].render_template(
            "website_event_sale_single_attendee.registration_attendee_details_single",
            {'tickets': tickets, 'event': event, 'availability_check': availability_check}
        )
