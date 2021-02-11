# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "CRM Event Category",
    "summary": "Link opportunities to event categories",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "category": "Event Management",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["crm", "event"],
    "data": [
        "reports/event_type_report_view.xml",
        "security/ir.model.access.csv",
        "views/crm_lead_view.xml",
        "views/event_type_view.xml",
    ],
}
