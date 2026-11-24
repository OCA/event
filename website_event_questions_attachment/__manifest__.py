# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Event Questions Attachment",
    "version": "18.0.1.0.0",
    "category": "Marketing",
    "author": "INVITU, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "license": "AGPL-3",
    "depends": ["website_event", "event"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/website_event_questions_attachment_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_event_questions_attachment/static/src/js/website_event_questions_attachment.js",
        ],
    },
    "installable": True,
}
