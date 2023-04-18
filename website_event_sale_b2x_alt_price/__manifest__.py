# Copyright 2021 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Online event ticket sales with alternative prices",
    "summary": "Display alt. price (B2B for B2C websites, and viceversa)",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "LGPL-3",
    "auto_install": True,
    "depends": ["website_event_sale", "website_sale_b2x_alt_price"],
    "data": ["templates/website_event_sale.xml"],
    "assets": {
        "web.assets_tests": [
            "/website_event_sale_b2x_alt_price/static/src/js/b2b.esm.js",
            "/website_event_sale_b2x_alt_price/static/src/js/b2c.esm.js",
        ]
    },
}
