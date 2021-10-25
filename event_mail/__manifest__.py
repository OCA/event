# Copyright 2017 Tecnativa - Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Event Mail",
    "summary": "Mail settings in events",
    "version": "14.0.1.0.0",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "depends": ["event"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_view.xml",
        "views/event_view.xml",
        "views/event_mail_view.xml",
    ],
    "installable": True,
}
