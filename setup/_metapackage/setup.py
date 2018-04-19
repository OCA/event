import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-event_contact',
        'odoo10-addon-event_mail',
        'odoo10-addon-event_project',
        'odoo10-addon-event_registration_mass_mailing',
        'odoo10-addon-event_registration_multi_qty',
        'odoo10-addon-event_session',
        'odoo10-addon-partner_event',
        'odoo10-addon-website_event_excerpt_img',
        'odoo10-addon-website_event_filter_selector',
        'odoo10-addon-website_event_share',
        'odoo10-addon-website_event_snippet_calendar',
        'odoo10-addon-website_event_type_description',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
