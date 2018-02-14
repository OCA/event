# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Excerpt + Image in Events",
    "summary": "New layout for event summary, including an excerpt and image",
    "version": "11.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, "
              "Onestein, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_event",
        "html_image_url_extractor",
        "html_text",
    ],
    "data": [
        "views/assets.xml",
        "views/event.xml",
        "views/event_event_view.xml",
    ],
    "images": [
        "images/frontend.png",
        "images/backend.png",
        "images/customize.png",
    ],
}
