# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Event Mail',
    'summary': 'Mail settings in events',
    'version': '10.0.1.0.0',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    'website': 'https://odoo-community.org/',
    'category': 'Marketing',
    'depends': ['event'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_view.xml',
        'views/event_view.xml',
        'views/event_mail_view.xml',
    ],
    'installable': True,
}
