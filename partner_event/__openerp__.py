# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Odoo Source Management Solution
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Javier Iniesta <javieria@antiun.com>
#                       Antonio Espinosa <antonioea@antiun.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Link partner to events',
    'version': '8.0.3.0.0',
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
}
