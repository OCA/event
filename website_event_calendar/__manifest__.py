{
    "name": "Events: generic & other calendar options",
    "version": "18.0.1.1.0",
    "category": "Marketing/Events",
    "summary": "Add generic and other calendar options to events "
    "(alongside the existing branded ones)",
    "author": "Onestein, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "license": "LGPL-3",
    "depends": [
        "website_event",
    ],
    "data": [
        "templates/website_event_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_event_calendar/static/src/scss/website.scss",
        ],
    },
}
