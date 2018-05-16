import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-event",
    description="Meta package for oca-event Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-partner_event',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
