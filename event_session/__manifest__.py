# Copyright 2017-19 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Event Sessions",
    "version": "14.0.1.1.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "summary": "Sessions in events",
    "depends": ["event_mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/event_session_security.xml",
        "views/event_session_view.xml",
        "views/event_view.xml",
        "wizards/wizard_event_session_view.xml",
    ],
    "installable": True,
}
