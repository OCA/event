# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Event Sale Sessions",
    "summary": "Sell Event Sessions",
    "version": "16.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "depends": ["event_sale", "event_session"],
    "data": [
        "views/event_session.xml",
        "views/sale_order.xml",
        "reports/sale_report.xml",
        "reports/event_sale_report.xml",
        "wizard/event_configurator.xml",
        "wizard/event_edit_registration.xml",
    ],
    "demo": ["demo/event_session.xml"],
    "assets": {
        "web.assets_backend": [
            "event_sale_session/static/src/js/*.esm.js",
        ],
    },
    "auto_install": True,
}
