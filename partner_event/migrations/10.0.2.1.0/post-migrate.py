# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.partner_event import post_init_hook


def migrate(cr, version):
    post_init_hook(cr, None)
