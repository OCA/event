import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-crm_event',
        'odoo13-addon-event_contact',
        'odoo13-addon-event_email_reminder',
        'odoo13-addon-event_mail',
        'odoo13-addon-event_registration_cancel_reason',
        'odoo13-addon-event_registration_multi_qty',
        'odoo13-addon-event_registration_partner_unique',
        'odoo13-addon-event_sale_registration_multi_qty',
        'odoo13-addon-event_sale_reservation',
        'odoo13-addon-event_sale_session',
        'odoo13-addon-event_session',
        'odoo13-addon-event_session_registration_multi_qty',
        'odoo13-addon-event_track_location_overlap',
        'odoo13-addon-event_type_multi_company',
        'odoo13-addon-partner_event',
        'odoo13-addon-website_event_crm',
        'odoo13-addon-website_event_filter_city',
        'odoo13-addon-website_event_questions_by_ticket',
        'odoo13-addon-website_event_questions_free_text',
        'odoo13-addon-website_event_require_login',
        'odoo13-addon-website_event_sale_b2x_alt_price',
        'odoo13-addon-website_event_sale_hide_ticket',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
