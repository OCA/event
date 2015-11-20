# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

{
    "name": "Training",
    "version": "8.0.3.0.0",
    "category": "Events",
    "author": "Grupo ESOC Ingeniería de Servicios, S.L.U., "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "http://www.grupoesoc.es",
    "installable": True,
    "application": True,
    "summary": "Extend events with training capabilities",
    "depends": [
        "partner_event",
        "product",
        "report",
    ],
    "data": [
        "data/training.duration_type.csv",
        "data/training.course_type.csv",
        "security/training.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",  # Must be loaded first
        "views/course.xml",
        "views/course_type.xml",
        "views/diploma_delivery_receipt_report.xml",
        "views/diploma_report.xml",
        "views/duration_type.xml",
        "views/event.xml",
        "views/event_registration.xml",
        "views/product_delivery_receipt_report.xml",
        "views/training_attendance_certificate_report.xml",
    ],
    "demo": [
        "demo/training.course.csv",
        "demo/training.duration.csv",
        "demo/event.event.csv",
    ],
}
