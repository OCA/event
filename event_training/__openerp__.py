# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

{
    "name": "Training",
    "version": "8.0.1.0.0",
    "category": "Events",
    "author": "Grupo ESOC Ingeniería de Servicios, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://grupoesoc.es",
    "installable": True,
    "application": True,
    "summary": "Extend events with training capabilities",
    "depends": [
        "event_product",
        "partner_event",
        "report",
    ],
    "data": [
        "security/event_training.yml",
        "views/diploma_delivery_receipt_report.xml",
        "views/diploma_report.xml",
        "views/event_event_view.xml",
        "views/event_registration_view.xml",
        "views/event_type_view.xml",
        "views/product_template_view.xml",
        "views/training_attendance_certificate_report.xml",
    ],
    "demo": [
        "demo/event_training_demo.yml",
    ],
}
