# Copyright 2023 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Website Event Sale Joined Constraint Single Attendee",
    "summary": "Glue module to be able to use both website_event_sale_joined_constraint "
    "and website_event_sale_single_attendee modules",
    "version": "15.0.1.0.0",
    "development_status": "Alpha",
    "category": "Website/Website",
    "website": "https://github.com/OCA/event",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "website_event_sale_joined_constraint",
        "website_event_sale_single_attendee",
    ],
    "data": [],
}
