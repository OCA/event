# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Event Selection Filters",
    "summary": "Add a customizable top area to filter events with selectors",
    "version": "9.0.1.0.1",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, "
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
    ],
    "images": [
        "images/all.png",
        "images/choose.png",
    ],
}
