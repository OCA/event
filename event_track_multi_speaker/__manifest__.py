# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Event Track Multi Speaker",
    "summary": """
        Allow for several speaker on event tracks""",
    "version": "16.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/OCA/event",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": ["website_event_track"],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "views/event_track.xml",
        "views/event_track_speaker.xml",
        "views/event_event.xml",
        "views/menuitems.xml",
    ],
    "demo": [],
    "qweb": [],
}
