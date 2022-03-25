# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def rename_event_session_seats(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE event_session
        ADD COLUMN seats_limited boolean""",
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE event_session
        SET seats_limited = CASE
            WHEN seats_availability = 'limited' THEN TRUE ELSE FALSE END""",
    )


@openupgrade.migrate()
def migrate(env, version):
    rename_event_session_seats(env)
