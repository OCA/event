# Copyright 2025 APSL-Nagarro Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Event No Index",
    "summary": "Prevent indexing unpublished event on website",
    "version": "14.0.1.0.0",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "APSL-Nagarro, Odoo Community Association (OCA)",
    "maintainers": ["peluko00"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_event",
    ],
    "data": [
        "views/website_templates.xml",
    ],
}
