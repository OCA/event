# Copyright 2016-2017 Tecnativa - Jairo Llopis
# Copyright 2019 Tecnativa - Cristina Martin R.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Event Filter City",
    "summary": "Add a customizable top area to filter events with city",
    "version": "15.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Antiun Ingeniería S.L., "
    "Tecnativa, "
    "Onestein, "
    "Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "LGPL-3",
    "installable": True,
    "depends": ["website_event"],
    "data": ["templates/event.xml"],
    "demo": ["demo/tour_data.xml"],
    "assets": {
        "web.assets_tests": [
            "/website_event_filter_city/static/src/js/*.js",
        ]
    },
}
