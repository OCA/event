# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Link partner to events',
    'version': '8.0.3.1.0',
    'category': 'Marketing',
    'author': 'Serv. Tecnol. Avanzados - Pedro M. Baeza, '
              'Antiun Ingeniería S.L., '
              'Tecnativa,'
              'Odoo Community Association (OCA)',
    'website': 'http://www.tecnativa.com',
    'depends': [
        'event',
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/event_event_view.xml',
        'views/event_registration_view.xml',
        'wizard/res_partner_register_event_view.xml',
    ],
    "installable": True,
    'license': 'AGPL-3',
}
