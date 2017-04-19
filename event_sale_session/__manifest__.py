# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Event Sale Sessions',
    'version': '10.0.1.0.0',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    'website': 'https://odoo-community.org/',
    'category': 'Marketing',
    'summary': 'Sessions sales in events',
    'depends': [
        'event_sale',
        'event_session',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/event_view.xml',
        'views/event_session_view.xml',
        'wizard/event_edit_registration.xml',
    ],
    'installable': True,
}
