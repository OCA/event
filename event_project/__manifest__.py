# Copyright 2015 Antiun - Javier Iniesta
# Copyright 2015 Antiun - Endika Iglesias
# Copyright 2015 Tecnativa - Antonio Espinosa
# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Event project",
    "version": "14.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "license": "AGPL-3",
    "category": "Event Management",
    "depends": ["event", "project_recalculate"],
    "data": [
        "views/event_event_view.xml",
        "views/project_project_view.xml",
        "views/project_task_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
