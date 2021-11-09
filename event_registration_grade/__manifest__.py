# Copyright 2021 Robin CORDIER
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Event Registration Grade",
    "version": "14.0.1.0.0",
    "category": "Event",
    "author": "Robin CORDIER," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "development_status": "Production/Stable",
    "license": "AGPL-3",
    'depends': [
        'base',
        'partner_event',
    ],
    'data': [
        'security/event_registration_grade.xml',
        'security/ir.model.access.csv',
        'data/event_registration_grade_data.xml',
        'data/email_template_data.xml',
        'views/event_registration_grade_views.xml',
        'views/event_views.xml',
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
