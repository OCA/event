# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Event Third Party",
    "summary": """
        Allows to define third parties involved in events with roles.""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://acsone.eu",
    "depends": [
        "event",
    ],
    "data": [
        "views/menu.xml",
        "security/event_third_party_role.xml",
        "views/event_third_party_role.xml",
        "views/event_event.xml",
        "security/event_third_party.xml",
        "views/event_third_party.xml",
        "report/report_paperformat.xml",
        "report/report_third_party.xml",
    ],
    "demo": [
        "demo/res_partner.xml",
        "demo/event_third_party_role.xml",
        "demo/event_third_party.xml",
    ],
}
