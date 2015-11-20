# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Sale Pro",
    "summary": "Extend event sales with more options",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "Grupo ESOC, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event_sale",
    ],
    "data": [
        "data/install.xml",
        "views/event_registration.xml",
        "views/quotation_generator.xml",
    ],
}
