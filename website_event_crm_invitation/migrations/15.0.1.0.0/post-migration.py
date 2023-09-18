# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_record_translations(
        env.cr,
        "website_event_crm",
        [
            "crm_lead_event_type_tpl",
        ],
    )
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "website_event_crm.crm_lead_event_type_tpl",
                "website_event_crm_invitation.crm_lead_event_type_tpl",
            )
        ],
    )
    openupgrade.load_data(
        env.cr,
        "website_event_crm_invitation",
        "migrations/15.0.1.0.0/noupdate_changes.xml",
    )
