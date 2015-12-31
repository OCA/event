# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

{
    "name": "Training Tracks",
    "summary": "Organize training tracks",
    "version": "8.0.1.0.0",
    "category": "Events",
    "author": "Grupo ESOC Ingeniería de Servicios, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://grupoesoc.es",
    "installable": True,
    "application": False,
    "auto_install": True,
    "depends": [
        "event_training",
        "website_event_track",
    ],
    "data": [
        "data/event.training.duration.type.csv",
        "data/event.type.csv",
        "security/ir.model.access.csv",
        "views/attendance_monitoring_report.xml",
        "views/duration_type_view.xml",
        "views/event_registration_view.xml",
        "views/event_track_view.xml",
        "views/event_type_view.xml",
        "views/product_template_view.xml",
        "wizards/wizard_summary_view.xml",
        "views/event_event_view.xml",
    ],
    "demo": [
        "demo/event.training.duration.csv",
    ],
}
