# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Register a lead directly in an event",
    "version": "8.0.1.2.0",
    "license": "AGPL-3",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "https://www.antiun.com",
    "category": "Event Management",
    "images": [
        "images/converting.png",
        "images/not_linked.png",
        "images/linked.png",
        "images/linking.png",
    ],
    "depends": [
        'crm',
        'event',
        'marketing_crm',
    ],
    "data": [
        'wizard/crm_lead_event_pick_view.xml',
        'wizard/crm_lead_to_opportunity_view.xml',
        'views/crm_lead_view.xml',
    ],
    "installable": True,
}
