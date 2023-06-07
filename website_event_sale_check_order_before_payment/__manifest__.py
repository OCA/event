# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Website Event Sale Check Order Before Payment",
    "summary": "Check one last time the sale order status before creating the payment "
    "transaction",
    "version": "13.0.1.0.0",
    "development_status": "Beta",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "license": "AGPL-3",
    "category": "Website/Website",
    "depends": ["website_event_sale"],
    "data": [
        "views/assets.xml",
        "views/payment_templates.xml",
        "views/res_config_settings_views.xml",
    ],
}
