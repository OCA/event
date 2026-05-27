# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Website Event Company Parent Visibility",
    "summary": "Subsidiaries' events shown on parent companies' websites "
    "(opt-in per subsidiary).",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "INVITU, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "depends": ["website_event"],
    "data": [
        "security/event_security.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
}
