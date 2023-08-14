# Copyright 2019 Tecnativa - Pedro M. Baeza
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Conditional Events Questions",
    "summary": "Events Questions conditional to the chosen ticket",
    "version": "13.0.1.0.1",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["website_event_sale", "website_event_questions"],
    "data": ["views/event_event_views.xml", "views/event_templates.xml"],
}
