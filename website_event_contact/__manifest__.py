# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Event Contacts",
    "version": "16.0.1.0.1",
    "summary": "Display your event contacts on your event page",
    "author": "Moduon,OpenSynergy Indonesia,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "category": "Marketing",
    "depends": ["website_event", "event_contact"],
    "data": [
        "views/event_templates_page_registration.xml",
        "views/snippets/snippets.xml",
    ],
    "application": False,
    "installable": True,
    "maintainers": ["Shide", "rafaelbn"],
    "license": "AGPL-3",
}
