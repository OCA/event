# Copyright 2016 Tecnativa - Sergio Teruel
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Event Email Reminder",
    "summary": "Send an email before an event start",
    "version": "15.0.1.0.0",
    "category": "Event Management",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["event"],
    "data": [
        "data/event_stage_data.xml",
        "data/ir_cron_data.xml",
        "data/mail_template_data.xml",
        "views/event_stage_views.xml",
    ],
}
