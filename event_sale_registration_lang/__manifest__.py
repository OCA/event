# Copyright 2021 Camptocamp (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Event Sale Registration Lang",
    "summary": "Allow to set attendee languages from Sale App",
    "version": "13.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["ivantodorovich"],
    "website": "https://github.com/OCA/event",
    "license": "AGPL-3",
    "category": "Marketing",
    "depends": ["event_sale", "event_registration_lang"],
    "data": ["wizards/registration_editor.xml"],
    "auto_install": True,
}
