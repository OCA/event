# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Event Type Description in Website",
    "summary": "Display a specific description for each event type",
    "version": "8.0.1.1.0",
    "category": "Website",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_event",
    ],
    "data": [
        "views/event_type_view.xml",
        "views/event.xml",
    ],
    "images": [
        "images/seminars.png",
        "images/all.png",
    ],
}
