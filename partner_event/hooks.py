# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, SUPERUSER_ID

LANG_OLD = "${object.partner_id.lang}"
LANG_NEW = "${object.attendee_partner_id.lang or object.partner_id.lang}"


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Fix computing of lang for affected templates
    tpls = env["mail.template"].search([
        ("model_id", "=", "event.registration"),
        ("lang", "=", LANG_OLD),
    ])
    tpls.write({
        "lang": LANG_NEW,
    })


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Restore computing of lang for affected templates
    tpls = env["mail.template"].search([
        ("model_id", "=", "event.registration"),
        ("lang", "=", LANG_NEW),
    ])
    tpls.write({
        "lang": LANG_OLD,
    })
