# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Products",
    "summary": "Combine products and events",
    "version": "8.0.1.0.0",
    "category": "Event Management",
    "website": "https://grupoesoc.es/",
    "author": "Grupo ESOC Ingeniería de Servicios, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event_sale",
    ],
    "data": [
        "views/event.xml",
        "views/product.xml",
    ]
}
