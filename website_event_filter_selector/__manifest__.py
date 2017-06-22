# -*- coding: utf-8 -*-
# Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Event Selection Filters",
    "summary": "Add a customizable top area to filter events with selectors",
    "version": "10.0.1.0.0",
    "category": "Website",
    "website": "https://www.tecnativa.com",
    "author": "Antiun Ingeniería S.L., "
              "Tecnativa, "
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
