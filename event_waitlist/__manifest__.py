# Copyright 2026 SportJoe GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Event Waitlist",
    "summary": "Waiting list for sold-out events with automatic promotion "
    "or time-limited seat offers",
    "version": "17.0.1.0.0",
    "category": "Marketing/Events",
    "website": "https://github.com/OCA/event",
    "author": "SportJoe GmbH, Odoo Community Association (OCA)",
    "maintainers": ["sebaodoo"],
    "license": "LGPL-3",
    "depends": ["event"],
    "data": [
        "security/event_waitlist_security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "data/mail_template_data.xml",
        "views/event_waitlist_views.xml",
        "views/event_event_views.xml",
        "views/event_waitlist_portal_templates.xml",
    ],
    "demo": ["demo/event_waitlist_demo.xml"],
}
