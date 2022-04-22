# Copyright 2016 Antiun Ingeniería S.L.
# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Cristina Martin
# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Reasons for event registrations cancellations",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "depends": ["event"],
    "data": [
        "security/ir.model.access.csv",
        "views/event_registration_view.xml",
        "wizard/event_registration_cancel_log_reason_view.xml",
    ],
    "installable": True,
}
