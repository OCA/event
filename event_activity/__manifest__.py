# Copyright 2021 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Event activities",
    "summary": "Allow activity management on events and registrations",
    "version": "12.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa - Jairo Llopis, Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["event", "mail"],
    "data": [
        "views/event_event.xml",
        "views/event_registration.xml",
    ],
}
