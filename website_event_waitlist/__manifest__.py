# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Website Event Waitlist",
    "summary": "Let visitors join the waiting list of sold-out events on the website",
    "version": "17.0.1.0.0",
    "category": "Marketing/Events",
    "website": "https://github.com/OCA/event",
    "author": "SportJoe GmbH, Odoo Community Association (OCA)",
    "maintainers": ["sebaodoo"],
    "license": "LGPL-3",
    "auto_install": True,
    "depends": ["event_waitlist", "website_event"],
    "data": [
        "views/event_templates.xml",
    ],
}
