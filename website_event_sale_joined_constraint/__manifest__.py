# Copyright 2023 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Website Event Sale Joined Constraint",
    "summary": "Allow to add constraints on event ticket sold on the website",
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
        # Views
        "views/event_templates_page_registration.xml",
        "views/event_ticket_views.xml",
        "views/product_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_event_sale_joined_constraint/static/src/js"
            "/website_event_ticket_details.js",
        ],
    },
}
