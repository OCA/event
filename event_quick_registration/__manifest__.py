# Copyright 2022 Camptocamp SA
# @author Damien Crier damien.crier@camptocamp.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Event Quick Registration",
    "summary": "Create registration quickly",
    "version": "15.0.1.0.0",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "category": "Event",
    "depends": ["event_sale"],
    "data": ["wizard/event_quick_registration.xml", "views/event_event.xml"],
    "installable": True,
}
