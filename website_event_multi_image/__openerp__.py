# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Multi images for events in website",
    "summary": "Show a gallery of images per event in their website",
    "version": "8.0.1.0.0",
    "category": "Event Management",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event_multi_image",
        "website_event",
        "website_multi_image",
    ],
    "data": [
        "views/event_templates.xml",
    ],
    "images": [
        "images/carousel.png",
        "images/thumbnail.png",
    ],
}
