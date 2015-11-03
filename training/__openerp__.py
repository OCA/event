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
        "partner_event",
        "report",
    ],
    "data": [
        "data/training.duration_type.csv",
        "data/training.action_type.csv",
        "data/training.material_type.csv",
        "data/training.material.csv",
        "security/training.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",  # Must be loaded first
        "views/action.xml",
        "views/action_type.xml",
        "views/duration_type.xml",
        "views/event.xml",
        "views/event_registration.xml",
        "views/material.xml",
        "views/material_type.xml",
        "report/diploma.xml",
        "report/diploma_delivery_receipt.xml",
        "report/training_attendance_certificate.xml",
    ],
    "demo": [
        "demo/training.action.csv",
        "demo/training.duration.csv",
        "demo/event.event.csv",
    ],
}
