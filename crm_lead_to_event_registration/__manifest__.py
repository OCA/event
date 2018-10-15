# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Cristina Martin
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Register a lead directly in an event",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "depends": [
        'crm',
        'event',
    ],
    "data": [
        'wizard/crm_lead_event_pick_view.xml',
        'wizard/crm_lead_to_opportunity_view.xml',
        'views/crm_lead_view.xml',
    ],
    "installable": True,
}
