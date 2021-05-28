# Copyright 2021 Camptocamp (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Event Registration Language",
    "summary": "Allows to set attendee languages",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["ivantodorovich"],
    "depends": ["event"],
    "data": ["views/event_registration.xml"],
    "post_init_hook": "post_init_hook",
}
