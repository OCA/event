# Copyright 2019 Tecnativa - Pedro M. Baeza
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Free Text Answers on Events Questions",
    "version": "13.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "website_event_questions",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/event_event_views.xml",
        "views/event_templates.xml",
    ],
}
