# Copyright 2017-19 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Multiple Dates per Track",
    "version": "16.0.1.0.0",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "summary": "Multiple Dates per Track",
    "depends": ["website_event_track"],
    "data": [
        "security/ir.model.access.csv",
        "views/event_track.xml",
    ],
    "installable": True,
}
