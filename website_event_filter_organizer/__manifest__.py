# Copyright 2019 Tecnativa - Sergio Teruel
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Website Event Filter Organizer',
    'summary': 'Filter events by organizer in frontend',
    'version': '12.0.1.0.0',
    'category': "event",
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/event',
    'depends': ['website_event'],
    'data': [
        'views/website_event.xml',
    ],
    'demo': [
        'demo/assets.xml',
    ],
    'installable': True,
}
