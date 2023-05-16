import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-crm_event>=15.0dev,<15.1dev',
        'odoo-addon-event_email_reminder>=15.0dev,<15.1dev',
        'odoo-addon-event_quick_registration>=15.0dev,<15.1dev',
        'odoo-addon-event_registration_cancel_reason>=15.0dev,<15.1dev',
        'odoo-addon-event_registration_mail_compose>=15.0dev,<15.1dev',
        'odoo-addon-event_registration_partner_unique>=15.0dev,<15.1dev',
        'odoo-addon-event_registration_qr_code>=15.0dev,<15.1dev',
        'odoo-addon-event_sale_reservation>=15.0dev,<15.1dev',
        'odoo-addon-event_sale_session>=15.0dev,<15.1dev',
        'odoo-addon-event_session>=15.0dev,<15.1dev',
        'odoo-addon-event_track_location_overlap>=15.0dev,<15.1dev',
        'odoo-addon-partner_event>=15.0dev,<15.1dev',
        'odoo-addon-sale_crm_event_reservation>=15.0dev,<15.1dev',
        'odoo-addon-website_event_filter_city>=15.0dev,<15.1dev',
        'odoo-addon-website_event_require_login>=15.0dev,<15.1dev',
        'odoo-addon-website_event_sale_b2x_alt_price>=15.0dev,<15.1dev',
        'odoo-addon-website_event_sale_cart_quantity_readonly>=15.0dev,<15.1dev',
        'odoo-addon-website_event_ticket_published>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
