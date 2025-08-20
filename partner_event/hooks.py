# Copyright 2019 David Vidal
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html


def post_init_hook(env):
    """Preload proper attendee partner for existing registrations using
    the same rules the module does"""
    attendees_emails = env["event.registration"].read_group(
        [("email", "!=", False)], ["email"], groupby="email"
    )
    for email in attendees_emails:
        # Order was done for avoiding extra queries for sorting the results
        attendee_partner = env["res.partner"].search(
            [("email", "=ilike", email["email"])], limit=1, order="id"
        )
        if attendee_partner:
            attendees = env["event.registration"].search(email["__domain"])
            attendees.write({"attendee_partner_id": attendee_partner.id})
