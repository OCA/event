# Copyright 2026 Riccardo Fiore
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    registration_mode = fields.Selection(
        selection=[
            ("native", "Native ticketing"),
            ("free", "Free / No registration"),
            ("external", "External registration"),
        ],
        default="native",
        required=True,
        help=(
            "How attendees register for this event on the website:\n"
            "- Native ticketing: use Odoo's built-in tickets and registration.\n"
            "- Free / No registration: show a custom message instead of tickets.\n"
            "- External registration: redirect attendees to a foreign ticket "
            "portal."
        ),
    )
    free_event_text = fields.Html(
        string="Free Event Message",
        translate=True,
        sanitize_attributes=True,
        help="Message displayed on the event page when the registration mode "
        "is 'Free / No registration'.",
    )
    external_ticket_url = fields.Char(
        string="External Ticket URL",
        help="Address of the external ticketing portal attendees are sent to "
        "when the registration mode is 'External registration'.",
    )
    external_button_text = fields.Char(
        translate=True,
        default="Get Tickets",
        help="Label of the button that links to the external ticketing portal.",
    )
    keep_custom_text_when_closed = fields.Boolean(
        default=False,
        help="Once registrations close (the event has ended, is sold out or "
        "was cancelled), Odoo normally shows its standard 'Registrations "
        "Closed' notice. Enable this to keep showing this event's custom "
        "content instead: the free event message or the external ticket "
        "button.",
    )
