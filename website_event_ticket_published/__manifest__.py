# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Website Event Ticket Published",
    "summary": "Allow to unpublish event ticket from the website",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Website/Website",
    "website": "https://github.com/OCA/event",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website_event"],
    "data": ["views/event_ticket.xml", "templates/event_ticket.xml"],
}
