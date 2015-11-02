# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

{
    "name": "Training Tracks",
    "version": "8.0.1.1.1",
    "category": "Project",
    "author": "Grupo ESOC",
    "license": "AGPL-3",
    "website": "http://www.grupoesoc.es",
    "installable": True,
    "application": False,
    "auto_install": True,
    "summary": "Organize training tracks",
    "depends": [
        "training",
        "website_event_track",
    ],
    "data": [
        "views/event_track_view.xml",
        "views/attendance_monitoring_report.xml",
    ],
    "demo": [
        "demo/event.track.csv",
    ],
}
