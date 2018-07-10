# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Mass mailing from events",
    'category': 'Marketing',
    'version': '11.0.1.0.1',
    'depends': [
        'mass_mailing_event',
    ],
    'data': [
        'views/event_registration.xml',
        'wizard/event_registration_mail_list_wizard.xml',
    ],
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': True,
}
