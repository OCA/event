import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-crm_lead_to_event_registration',
        'odoo11-addon-event_registration_cancel_reason',
        'odoo11-addon-event_registration_mass_mailing',
        'odoo11-addon-event_registration_partner_unique',
        'odoo11-addon-event_session',
        'odoo11-addon-partner_event',
        'odoo11-addon-website_event_excerpt_img',
        'odoo11-addon-website_event_filter_selector',
        'odoo11-addon-website_event_questions_by_ticket',
        'odoo11-addon-website_event_questions_free_text',
        'odoo11-addon-website_event_require_login',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
