# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Event Require Legal",
    "version": "16.0.1.0.0",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "category": "Event",
    "depends": ["website_event"],
    "data": [
        "views/event_views.xml",
        "views/event_templates_page_registration.xml",
    ],
    "assets": {
        "web.assets_tests": [
            "/website_event_require_legal/static/tests/tours/tour.js",
        ],
    },
    "installable": True,
    "license": "AGPL-3",
}
