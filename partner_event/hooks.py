# Copyright 2019 David Vidal
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """Preload proper attendee partner for existing registrations using
    the same rules the module does"""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        attendees_emails = env["event.registration"].read_group(
            [("email", "!=", False)], ["email"], groupby="email"
        )
        for email in attendees_emails:
            attendee_partner = env["res.partner"].search(
                [("email", "=ilike", email["email"])], limit=1
            )
            if attendee_partner:
                attendees = env["event.registration"].search(email["__domain"])
                attendees.write({"attendee_partner_id": attendee_partner.id})
