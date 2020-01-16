# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Unique Partner per Event",
    "summary": "Enforces 1 registration per partner and event",
    "version": "13.0.1.0.0",
    "category": "Marketing",
    "website": "https://github.com/oca/event",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event",
        "partner_event",
    ],
    "data": [
        "views/event_event_view.xml",
    ],
}
