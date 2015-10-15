# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

{
    "name": "Training",
    "version": "8.0.3.0.0",
    "category": "Project",
    "author": "Grupo ESOC",
    "license": "AGPL-3",
    "website": "http://www.grupoesoc.es",
    "installable": True,
    "application": True,
    "summary": "Extend events with training capabilities",
    "depends": [
        "event",
        "report",
    ],
    "data": [
        "data/training.duration_type.csv",
        "data/training.action_type.csv",
        "security/training.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/event.xml",
        "views/action_type.xml",
        "views/diploma.xml",
        "views/action.xml",
        "views/duration_type.xml",
    ],
    "demo": [
        "demo/training.action.csv",
        "demo/training.duration.csv",
        "demo/event.event.csv",
    ],
}
