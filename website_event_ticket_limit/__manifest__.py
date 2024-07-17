{
    "name": "Website Event Ticket Limit",
    "version": "16.0.1.0.0",
    "author": "Le Filament, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "application": False,
    "category": "Marketing",
    "depends": ["website_event"],
    "data": [
        "templates/event_templates_registration.xml",
        "views/event_ticket_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
