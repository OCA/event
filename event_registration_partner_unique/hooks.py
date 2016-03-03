# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, exceptions


def pre_init_hook(cr):
    """Ensure no duplicates before installing."""
    cr.execute("""
        SELECT
            event_event.name,
            res_partner.name,
            COUNT(*) AS duplicates
        FROM
            event_registration

            INNER JOIN event_event
            ON event_event.id = event_registration.event_id

            INNER JOIN res_partner
            ON res_partner.id = event_registration.partner_id
        GROUP BY
            event_registration.event_id,
            event_event.name,
            event_registration.partner_id,
            res_partner.name
        HAVING
            COUNT(*) > 1
    """)
    rows = cr.fetchall()
    if rows:
        message = _("Event %s; Partner %s; %d duplicates.")
        details = "\n".join(message % row for row in rows)
        raise exceptions.ValidationError(
            _("Remove duplicates before installing:\n%s") % details)


def post_init_hook(cr, registry):
    """Using custom unique indexes because of null values in tickets.

    See http://stackoverflow.com/a/8289253/1468388.
    """
    indexes = (
        """
            CREATE UNIQUE INDEX
            event_registration_unique_partner_ticket_null
            ON event_registration (partner_id, event_id)
            WHERE event_ticket_id IS NULL
        """,
        """
            CREATE UNIQUE INDEX
            event_registration_unique_partner_ticket_fill
            ON event_registration (partner_id, event_id, event_ticket_id)
            WHERE event_ticket_id IS NOT NULL
        """,
    )
    for index in indexes:
        cr.execute(index)


def uninstall_hook(cr, registry):
    """Remove manual unique indexes."""
    cr.execute(
        "DROP INDEX IF EXISTS event_registration_unique_partner_ticket_null")
    cr.execute(
        "DROP INDEX IF EXISTS event_registration_unique_partner_ticket_fill")
