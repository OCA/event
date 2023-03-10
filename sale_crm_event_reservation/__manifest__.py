# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Create event quotations from opportunities",
    "summary": "Combine event reservations, opportunities and quotations",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": ["crm_event", "event_sale_reservation", "sale_crm"],
    "data": [
        "reports/event_type_report_views.xml",
        "security/ir.model.access.csv",
        "wizards/crm_lead_event_sale_wizard_views.xml",
        "views/crm_lead_views.xml",
    ],
}
