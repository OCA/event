# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Event Sale Update Qty",
    "summary": "Update event registrations from confirmed sale order lines.",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["pilarvargas-tecnativa"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["event_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "wizards/event_sale_update_qty_wizard.xml",
    ],
}
