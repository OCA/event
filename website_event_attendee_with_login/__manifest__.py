# Copyright 2019 Chris Mann - github.com/chrisandrewmann
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Website Event Attendee With Login',
    'version': '12.0.1.0.0',
    'author': 'Chris Mann, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/event',
    'category': 'Event',
    'depends': [
        'website_event'
    ],
    'data': [
        'views/event_views.xml',
        'views/website_event_registration_attendee_details_views.xml',
        'views/website_registration_template_views.xml'
    ],
    'installable': True,
    'license': 'AGPL-3',
}
