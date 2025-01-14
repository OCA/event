# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sell event reservations",
    "summary": "Allow selling event registrations before the event exists",
    "version": "17.0.1.0.1",
    "development_status": "Mature",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["pilarvargas-tecnativa"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event_sale",
    ],
    "data": [
        "reports/sale_report_view.xml",
        "wizards/registration_editor_view.xml",
        "views/event_type_view.xml",
        "views/product_template_view.xml",
        "views/sale_order_view.xml",
    ],
}
