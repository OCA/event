import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-event_email_reminder',
        'odoo12-addon-event_mail',
        'odoo12-addon-event_registration_multi_qty',
        'odoo12-addon-event_track_location_overlap',
        'odoo12-addon-partner_event',
        'odoo12-addon-website_event_filter_organizer',
        'odoo12-addon-website_event_filter_selector',
        'odoo12-addon-website_event_share',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
