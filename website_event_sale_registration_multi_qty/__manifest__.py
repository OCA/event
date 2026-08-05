# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Website Event Registration Multi Qty",
    "summary": "Allow registration of multiple quantities via website",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Marketing/Events",
    "website": "https://github.com/OCA/event",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "website_event_sale",
        "event_sale_registration_multi_qty",
    ],
    "data": [
        "templates/website_event.xml",
    ],
    "demo": [
        "demo/event_event.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/website_event_sale_registration_multi_qty/static/src/"
            "EventRegistrationForm.esm.js",
        ],
    },
}
