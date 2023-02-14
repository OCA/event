# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sell event reservations",
    "summary": "Allow selling event registrations before the event exists",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event_sale",
        "web_ir_actions_act_multi",
        "web_ir_actions_act_view_reload",
    ],
    "data": [
        "reports/sale_report_view.xml",
        "wizards/registration_editor_view.xml",
        "views/event_type_view.xml",
        "views/product_template_view.xml",
        "views/sale_order_view.xml",
    ],
}
