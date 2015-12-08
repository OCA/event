# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Legal terms per event",
    "summary": "Make attendees to accept legal terms per event",
    "version": "8.0.1.0.0",
    "category": "Marketing",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "website_event_sale",
        "website_sale_product_legal",
    ],
    "data": [
        "views/event_event_view.xml",
        "views/legal_term_view.xml",
        "views/templates.xml",
    ],
}
