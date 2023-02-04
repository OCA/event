import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-event_email_reminder>=15.0dev,<15.1dev',
        'odoo-addon-event_quick_registration>=15.0dev,<15.1dev',
        'odoo-addon-event_registration_mail_compose>=15.0dev,<15.1dev',
        'odoo-addon-event_registration_qr_code>=15.0dev,<15.1dev',
        'odoo-addon-partner_event>=15.0dev,<15.1dev',
        'odoo-addon-website_event_sale_cart_quantity_readonly>=15.0dev,<15.1dev',
        'odoo-addon-website_event_ticket_published>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
