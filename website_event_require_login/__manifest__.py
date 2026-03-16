# Copyright 2019 Tecnativa - David Vidal
# Copyright 2026 TechnoLibre - Mathieu Benoit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Event Require Login",
    "version": "18.0.1.0.0",
    "author": "Tecnativa, " "Odoo Community Association (OCA), " "TechnoLibre",
    "website": "https://github.com/OCA/event",
    "category": "Event",
    "depends": ["website_event"],
    "data": ["views/event_views.xml", "views/website_event_templates.xml"],
    "assets": {
        "web.assets_frontend": [
            "website_event_require_login/static/src/js/registration_login_required.esm.js",
        ],
        "web.assets_tests": [
            "/website_event_require_login/static/tests/tours/*",
        ],
    },
    "installable": True,
    "license": "AGPL-3",
}
