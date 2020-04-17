{
    'name': 'Custom Events',
    'category': 'Website',
    'summary': "Customization of Event registration",
    "version": "12.0.0.0.5",
    'author': 'ArcheTI',
    'website': 'http://archeti.ca',
    'depends': [
        'website_event',
        'website_event_sale',
        'event_sale',
        'event_session',
        'event_sale_session',
    ],
    'data': [
        'views/event_templates.xml',
        'security/acl.xml',
        'security/ir_rules.xml',
    ],
    'application': False,
}
