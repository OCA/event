# -*- coding: utf-8 -*-
# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Unique Partner per Event",
    "summary": "Enforces 1 registration per partner and event",
    "version": "9.0.1.0.0",
    "category": "Events",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event",
    ],
    "data": [
        "views/event_event_view.xml",
    ],
}
