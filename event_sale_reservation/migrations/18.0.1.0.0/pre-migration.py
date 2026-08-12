# Copyright 2026 Heliconia Solutions Pvt Ltd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.map_values(
        env.cr,
        "detailed_type",
        "service_tracking",
        [("event_reservation", "event_reservation")],
        table="product_template",
    )
