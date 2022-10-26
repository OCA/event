# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Website Event Sale Single Attendee",
    "summary": "Register a single attendee for multiple tickets",
    "version": "15.0.1.0.0",
    "development_status": "Alpha",
    "category": "Website/Website",
    "website": "https://github.com/OCA/event",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_event_sale",
    ],
    "data": [
        "templates/event_templates.xml",
        "views/event_event.xml",
        "views/event_type.xml",
    ],
}
