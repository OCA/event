# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Event Type Description in Website",
    "summary": "Display a specific description for each event type",
    "version": "12.0.1.0.0",
    "category": "Website",
    "website": "https://www.tecnativa.com",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_event",
    ],
    "data": [
        "views/event_type_view.xml",
        "views/event.xml",
    ],
    "images": [
        "images/seminars.png",
        "images/all.png",
    ],
}
