import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-event_badge_design',
        'odoo14-addon-event_contact',
        'odoo14-addon-event_mail',
        'odoo14-addon-event_project',
        'odoo14-addon-event_registration_cancel_reason',
        'odoo14-addon-event_registration_mass_mailing',
        'odoo14-addon-event_registration_multi_qty',
        'odoo14-addon-event_registration_partner_unique',
        'odoo14-addon-event_registration_qr_code',
        'odoo14-addon-event_sale_registration_multi_qty',
        'odoo14-addon-event_sale_session',
        'odoo14-addon-event_session',
        'odoo14-addon-event_session_registration_multi_qty',
        'odoo14-addon-partner_event',
        'odoo14-addon-website_event_questions_by_ticket',
        'odoo14-addon-website_event_questions_template',
        'odoo14-addon-website_event_require_login',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
