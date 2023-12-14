{
    "name": "Le Filament - Website event copy",
    "summary": "Allow website linked to an event to be copied "
    "when the event is duplicated",
    "author": "Le Filament, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "event_session",
        "website_event",
    ],
    "data": [
        "security/ir.model.access.csv",
        # datas
        # views
        "views/event_views.xml",
        # views menu
        # wizard
    ],
    "assets": {
        "web._assets_primary_variables": [],
        "web._assets_frontend_helpers": [],
        "web.assets_frontend": [],
        "web.assets_tests": [],
        "web.assets_qweb": [],
    },
    "installable": True,
    "auto_install": False,
}
