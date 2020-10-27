import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-event_registration_cancel_reason',
        'odoo13-addon-event_registration_partner_unique',
        'odoo13-addon-partner_event',
        'odoo13-addon-website_event_questions_by_ticket',
        'odoo13-addon-website_event_require_login',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
