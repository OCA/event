# Copyright 2019 Tecnativa - Pedro M. Baeza

from openupgradelib import openupgrade, openupgrade_120


@openupgrade.migrate()
def migrate(env, version):
    openupgrade_120.convert_field_bootstrap_3to4(
        env, 'event.type', 'description',
    )
