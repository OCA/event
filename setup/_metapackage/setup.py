import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-event_mail>=16.0dev,<16.1dev',
        'odoo-addon-event_registration_mass_mailing>=16.0dev,<16.1dev',
        'odoo-addon-event_registration_multi_qty>=16.0dev,<16.1dev',
        'odoo-addon-event_registration_partner_unique>=16.0dev,<16.1dev',
        'odoo-addon-event_sale_registration_multi_qty>=16.0dev,<16.1dev',
        'odoo-addon-event_sale_session>=16.0dev,<16.1dev',
        'odoo-addon-event_session>=16.0dev,<16.1dev',
        'odoo-addon-event_session_registration_multi_qty>=16.0dev,<16.1dev',
        'odoo-addon-partner_event>=16.0dev,<16.1dev',
        'odoo-addon-website_event_questions_by_ticket>=16.0dev,<16.1dev',
        'odoo-addon-website_event_require_login>=16.0dev,<16.1dev',
        'odoo-addon-website_event_sale_cart_quantity_readonly>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
