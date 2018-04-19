import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-crm_lead_to_event_registration',
        'odoo8-addon-event_contact',
        'odoo8-addon-event_email_reminder',
        'odoo8-addon-event_kanban_view_optimized',
        'odoo8-addon-event_multi_image',
        'odoo8-addon-event_product',
        'odoo8-addon-event_project',
        'odoo8-addon-event_registration_cancel_reason',
        'odoo8-addon-event_registration_mass_mailing',
        'odoo8-addon-event_registration_partner_unique',
        'odoo8-addon-event_registration_seat_limit',
        'odoo8-addon-event_sale_extra_info',
        'odoo8-addon-event_sale_registration_partner_unique',
        'odoo8-addon-event_track_generate',
        'odoo8-addon-partner_event',
        'odoo8-addon-website_event_contact',
        'odoo8-addon-website_event_excerpt_img',
        'odoo8-addon-website_event_filter_selector',
        'odoo8-addon-website_event_sale_legal',
        'odoo8-addon-website_event_share',
        'odoo8-addon-website_event_type_description',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
