# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Event Sale Sessions",
    "summary": "Sessions sales in events",
    "version": "14.0.1.0.1",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "depends": ["event_sale", "event_session"],
    "data": [
        "security/ir.model.access.csv",
        "reports/sale_report_views.xml",
        "views/assets.xml",
        "views/sale_order_views.xml",
        "views/event_view.xml",
        "views/event_session_view.xml",
        "wizard/event_edit_registration.xml",
        "wizard/event_configurator_views.xml",
    ],
    "installable": True,
}
