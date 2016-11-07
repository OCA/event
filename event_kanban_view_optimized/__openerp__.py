# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Event kanban view optimized",
    "summary": "Optimize event kanban view load time",
    "version": "8.0.1.0.0",
    "category": "Event Management",
    "website": "https://odoo-community.org/",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event",
    ],
    "data": [
        "views/event_event_view.xml",
    ],
}
