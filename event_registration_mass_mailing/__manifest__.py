# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Put event registrations emails into mailing lists",
    "category": "Marketing",
    "version": "14.0.1.0.0",
    "depends": ["event", "mass_mailing"],
    "data": [
        "security/ir.model.access.csv",
        "views/event_registration.xml",
        "wizard/event_registration_mail_list_wizard.xml",
    ],
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
}
