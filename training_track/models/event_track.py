# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import fields, models


class EventTrack(models.Model):
    """Expand event tracks with training duration types.

    This is used to calculate how many hours of each type have been fulfilled.
    """
    _inherit = "event.track"

    duration_type_id = fields.Many2one(
        "training.duration_type",
        "Training hour type",
        help="Training hour type of this track, if it belongs to a training "
             "group.")
