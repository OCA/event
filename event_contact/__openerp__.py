# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Event Contacts',
    'version': '8.0.1.0.0',
    'summary': 'Add contacts to event and event type',
    'author': 'OpenSynergy Indonesia, '
              'Antiun Ingeniería S.L., '
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
