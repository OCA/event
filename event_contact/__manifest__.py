# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Event Contacts',
    'version': '10.0.1.0.0',
    'summary': 'Add contacts to event and event type',
    'author': 'OpenSynergy Indonesia, '
              'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://opensynergy-indonesia.com',
    'category': 'Marketing',
    'depends': ['event'],
    'data': [
        'views/event_event_view.xml',
        'views/event_type_view.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
