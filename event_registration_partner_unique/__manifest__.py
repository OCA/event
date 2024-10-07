# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Cristina Martin R.
# Copyright 2020 Tecnativa - Víctor Martínez
# Copyright 2023 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Unique Partner per Event",
    "summary": "Enforces 1 registration per partner and event",
    "version": "16.0.1.0.0",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["event", "partner_event"],
    "data": ["views/event_event_view.xml", "views/event_type_view.xml"],
}
