# Copyright 2018 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Event Calendar and List Snippet and Iframe",
    "summary": "Browsable calendar with events list for your website",
    "version": "15.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website_event"],
    "data": ["templates/embed.xml", "templates/snippets.xml"],
    "assets": {
        "web.assets_frontend": [
            "website_event_snippet_calendar/static/src/css/style.scss",
            "website_event_snippet_calendar/static/src/js/animation.js",
        ],
        "website.assets_editor": [
            "website_event_snippet_calendar/static/src/js/options.js",
        ],
    },
}
