# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Event Sale Tracks',
    'summary': 'Sell Tickets by Tracks',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Others',
    'depends': [
        'event_sale',
        'website_event_track',
    ],
    'website': 'https://github.com/OCA/event',
    'data': [
        'views/event_ticket.xml',
        'views/event_views.xml',
        'views/event_track.xml',
        'views/event_registration.xml',
    ],
}
