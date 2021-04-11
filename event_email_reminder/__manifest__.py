# Copyright 2016 Tecnativa - Sergio Teruel
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Event Email Reminder",
    "summary": "Send an email before an event start",
    "version": "13.0.1.0.0",
    "category": "Event Management",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["event"],
    "data": ["data/event_email_reminder_data.xml"],
}
