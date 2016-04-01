# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Event Contacts',
    'version': '8.0.1.0.0',
    'summary': 'Publish your event contacts',
    'author': 'OpenSynergy Indonesia,Odoo Community Association (OCA)',
    'website': 'https://opensynergy-indonesia.com',
    'category': 'Marketing',
    'depends': [
        'website_event',
        'event_contact'
    ],
    'data': ['views/website_event_contact.xml'],
    'installable': True,
    'license': 'AGPL-3',
}
