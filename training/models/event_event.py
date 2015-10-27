# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import api, fields, models
from .common import M


class Event(models.Model):
    """Expand events with training actions.

    Events with a training type and a training action are considered training
    groups.
    """

    _inherit = "event.event"

    training_action_id = fields.Many2one(
        M % "action",
        "Training action",
        help="Training action of this event, if it is a training group.")

    @api.constrains("training_action_id")
    def _check_grade_limits(self):
        """Ensure no conflicts between limits and actual student grades."""
        self.registration_ids._check_grade_limits()
