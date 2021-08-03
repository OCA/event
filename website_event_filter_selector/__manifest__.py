# Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2019 Tecnativa - Cristina Martin R.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Event Selection Filters",
    "summary": "Add a customizable top area to filter events with selectors",
    "version": "12.0.1.2.1",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Antiun Ingeniería S.L., "
              "Tecnativa, "
              "Onestein, "
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_event",
    ],
    "data": [
        "templates/assets.xml",
        "templates/event.xml",
    ],
    "demo": [
        "demo/assets.xml",
        "demo/tour_data.xml",
    ],
}
