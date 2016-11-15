# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# © 2016 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Event Email Reminder",
    "summary": "Send an email before an event start",
    "version": "9.0.1.0.0",
    "category": "Event Management",
    'website': 'http://www.tecnativa.com',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event",
    ],
    "data": [
        "data/event_email_reminder_data.xml",
    ],
}
