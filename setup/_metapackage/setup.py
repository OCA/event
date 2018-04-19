import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-crm_lead_to_event_registration',
        'odoo9-addon-event_email_reminder',
        'odoo9-addon-event_registration_cancel_reason',
        'odoo9-addon-event_registration_mass_mailing',
        'odoo9-addon-event_registration_partner_unique',
        'odoo9-addon-partner_event',
        'odoo9-addon-website_event_filter_selector',
        'odoo9-addon-website_event_share',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
