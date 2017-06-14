# -*- coding: utf-8 -*-
# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models


class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    @api.model
    def _get_mailing_model(self):
        res = super(MassMailing, self)._get_mailing_model()
        res.append(('event.registration', _('Event Registrations')))
        return res
