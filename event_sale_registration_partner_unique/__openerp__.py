# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Unique Partner per Event, Combined With Event Sales",
    "summary": "Makes event sales not to duplicate registrations",
    "version": "8.0.1.0.0",
    "category": "Events",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "autoinstall": True,
    "depends": [
        "event_registration_partner_unique",
        "event_sale",
    ],
}
