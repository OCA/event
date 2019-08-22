# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Event Image',
    'version': '12.0.1.0.0',
    'author': 'Numigi, '
              'Odoo Community Association (OCA)',
    'maintainer': 'Numigi',
    'website': 'https://github.com/OCA/event',
    "license": "AGPL-3",
    'category': 'Marketing',
    'summary': 'Add Image field to event.',
    'depends': [
        'event',
    ],
    'data': [
        'views/event_form_view.xml',
    ],
    'installable': True,
}
