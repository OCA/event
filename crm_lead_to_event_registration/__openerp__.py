# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Register a lead directly in an event",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "Antiun Ingeniería S.L., "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Odoo Community Association (OCA)",
    "website": "https://www.antiun.com",
    "category": "Event Management",
    "depends": [
        'crm',
        'event',
    ],
    "data": [
        'wizard/crm_lead_to_opportunity_view.xml',
    ],
    "installable": True,
}
