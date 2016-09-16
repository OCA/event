# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Excerpt + Image in Events",
    "summary": "New layout for event summary, including an excerpt and image",
    "version": "8.0.1.1.0",
    "category": "Website",
    "website": "https://www.tecnativa.com",
    "author": "Antiun Ingeniería S.L., Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_event",
        "html_image_url_extractor",
        "html_text",
    ],
    "data": [
        "views/assets.xml",
        "views/event.xml",
        "views/event_event_view.xml",
    ],
    "images": [
        "images/frontend.png",
        "images/backend.png",
        "images/customize.png",
    ],
}
