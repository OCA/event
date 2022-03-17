# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Event Sale Registration Multi Qty",
    "version": "14.0.1.0.0",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "summary": "Allows sell registrations with more than one attendee",
    "depends": ["event_sale", "event_registration_multi_qty"],
    "data": ["wizards/event_edit_registration.xml"],
    "installable": True,
    "auto_install": True,
}
