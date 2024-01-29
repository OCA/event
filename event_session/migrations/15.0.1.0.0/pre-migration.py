# Copyright 2012 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _set_use_sessions_flag(env):
    """Preset the new use_sessions flag according to existing data"""
    openupgrade.logged_query(
        env.cr, "ALTER TABLE event_type ADD COLUMN IF NOT EXISTS use_sessions BOOLEAN"
    )
    openupgrade.logged_query(
        env.cr, "ALTER TABLE event_event ADD COLUMN IF NOT EXISTS use_sessions BOOLEAN"
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE event_event SET use_sessions = true
        WHERE id in (
            SELECT DISTINCT event_id FROM event_session
        )
    """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE event_type SET use_sessions = true
        WHERE id in (
            SELECT DISTINCT event_type_id FROM event_event WHERE use_sessions
        )
    """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _set_use_sessions_flag(env)
