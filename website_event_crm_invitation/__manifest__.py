# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website, event and CRM integration",
    "summary": "Invite leads to event types on website",
    "version": "15.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "AGPL-3",
    "installable": True,
    "depends": ["crm_event", "website_event"],
    "data": [
        "data/ir_cron_data.xml",
        "data/mail_template_data.xml",
        "views/crm_lead_view.xml",
        "views/crm_stage_view.xml",
    ],
}
