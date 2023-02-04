# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, "event_email_reminder", "migrations/15.0.1.0.0/noupdate_changes.xml"
    )
    openupgrade.delete_record_translations(
        env.cr,
        "event_email_reminder",
        ["event_email_reminder_template"],
    )
