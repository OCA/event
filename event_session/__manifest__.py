# Copyright 2017-19 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Event Sessions",
    "summary": "Sessions in events",
    "version": "16.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "depends": ["event"],
    "data": [
        "data/event_session_timeslot.xml",
        "data/mail_template.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/event_event.xml",
        "views/event_registration.xml",
        "views/event_session.xml",
        "views/event_type.xml",
        "reports/event_report_templates.xml",
        "wizards/wizard_event_session.xml",
    ],
    "demo": ["demo/event_session.xml"],
}
