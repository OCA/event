# -*- coding: utf-8 -*-
# © 2014 Tecnativa S.L. - Pedro M. Baeza
# © 2015 Tecnativa S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Antonio Espinosa
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Link partner to events',
    'version': '9.0.1.0.0',
    'category': 'Marketing',
    'author': 'Tecnativa,'
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
    'installable': True,
}
