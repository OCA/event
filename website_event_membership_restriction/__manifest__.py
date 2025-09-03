# Copyright 2024 Tecnativa - Pilar Vargas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Event Membership Restriction",
    "summary": "Restrict event registration to members only",
    "version": "18.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["website_event", "membership"],
    "data": [
        "data/website_event_membership_info.xml",
        "views/event_event_views.xml",
        "views/event_templates.xml",
    ],
}
