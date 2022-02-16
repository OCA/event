# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Event Registration Not Counting Seat",
    "summary": "Register attendee for an event but does not take one seat",
    "version": "13.0.1.0.0",
    "development_status": "Beta",
    "category": "Event",
    "website": "https://github.com/OCA/event",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["event_sale"],
    "data": ["views/event_ticket.xml", "views/event_registration.xml"],
}
