from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env,
        "event_email_reminder",
        "migrations/19.0.1.0.0/noupdate_changes.xml",
    )
    openupgrade.delete_record_translations(
        env.cr,
        "event_email_reminder",
        ["event_email_reminder_template"],
    )
