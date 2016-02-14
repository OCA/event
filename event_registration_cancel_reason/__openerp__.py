# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Reasons for event registrations cancellations",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "Antiun Ingeniería S.L., "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
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
