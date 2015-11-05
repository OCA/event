# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import fields, models


class DurationType(models.Model):
    """Know which durations need attendance monitoring."""
    _inherit = "training.duration_type"

    monitor_attendance = fields.Boolean(
        help="Does this duration type use attendance monitoring?")
