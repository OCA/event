# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Event Ribbon",
    "summary": """Add ribbons on events""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "depends": ["website_event"],
    "data": [
        "security/ir.model.access.csv",
        "views/event_event_ribbon.xml",
        "views/event_event.xml",
        "views/event_templates.xml",
    ],
    "demo": [],
}
