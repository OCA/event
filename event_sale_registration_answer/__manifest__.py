# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Event Sale Registration Answer",
    "summary": "Enter Answers to event Questions from the Sales Order",
    "version": "16.0.1.0.0",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "maintainers": ["dreispt"],
    "website": "https://github.com/OCA/event",
    "license": "AGPL-3",
    "category": "Others",
    "depends": ["event_sale", "website_event_questions"],
    "data": [
        "views/event_registration_answer_views.xml",
        "views/sale_order.xml",
    ],
}
