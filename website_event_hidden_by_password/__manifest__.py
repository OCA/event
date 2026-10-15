# Copyright 2026 Riccardo Fiore
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Event Hidden by Password",
    "summary": "Hide website events behind a per-event access password",
    "version": "19.0.1.0.0",
    "category": "Marketing/Events",
    "author": "Riccardo Fiore, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "license": "AGPL-3",
    "development_status": "Beta",
    "maintainers": ["odrakirmusic"],
    "depends": ["website_event"],
    "data": [
        "views/event_event_views.xml",
        "views/website_event_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_event_hidden_by_password/static/src/scss/website_event_hidden_by_password.scss",
        ],
    },
    "installable": True,
    "application": False,
}
