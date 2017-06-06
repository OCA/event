# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Event Sale Registration Multi Qty',
    'version': '10.0.1.0.0',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    'website': 'https://www.tecnativa.com',
    'category': 'Marketing',
    'summary': 'Allows sell registrations with more than one attendee',
    'depends': [
        'event_sale',
        'event_registration_multi_qty',
    ],
    'data': [
        'wizards/event_edit_registration.xml',
    ],
    'installable': True,
    'auto_install': True,
}
