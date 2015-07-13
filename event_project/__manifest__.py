# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

{
    "name": "Event project",
    "version": "8.0.1.1.0",
    "author": "Antiun Ingeniería S.L., "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Odoo Community Association (OCA)",
    "website": "http://www.antiun.com",
    "license": "AGPL-3",
    "category": "Event Management",
    "depends": [
        'event',
        'project_recalculate'
    ],
    'data': [
        "wizard/project_template_wizard.xml",
        "views/event_event_view.xml",
        "views/project_project_view.xml",
        "views/project_task_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': False,
}
