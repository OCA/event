# -*- coding: utf-8 -*-
# Copyright 2016 Antiun Ingeniería S.L.
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Reasons for event registrations cancellations",
    "version": "9.0.1.0.0",
    "license": "AGPL-3",
    "author": "Antiun Ingeniería S.L., "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "https://www.antiun.com",
    "category": "Event Management",
    "depends": [
        'event',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/event_registration_view.xml',
        'wizard/event_registration_cancel_log_reason_view.xml',
    ],
    "installable": True,
}
