# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

{
    "name": "Generate Training Tracks",
    "version": "8.0.1.0.0",
    "category": "Project",
    "author": "Grupo ESOC",
    "license": "AGPL-3",
    "website": "http://www.grupoesoc.es",
    "auto_install": True,
    "summary": "Insert automatically training tracks",
    "depends": [
        "event_track_generate",
        "training_track",
    ],
    "data": [
        "views/event_track_generate_generator_views.xml",
    ],
}
