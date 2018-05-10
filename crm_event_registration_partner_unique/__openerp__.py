# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Unique Partner per Event and CRM",
    "summary": "Avoids duplicates in events when partners are merged",
    "version": "9.0.1.0.0",
    "category": "Events",
    "website": "http://github.com/OCA/event",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "event_registration_partner_unique",
        "crm",
    ],
    "data": [
    ],
}
