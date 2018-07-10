# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    opt_out = fields.Boolean(
        string="Opt-Out", default=False,
        help="If opt-out is checked, this contact has refused to receive "
             "emails for mass mailing and marketing campaign.")
