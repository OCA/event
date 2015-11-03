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

    material_ids = fields.Many2many(
        M % "material",
        string="Materials",
        states={"done": [("readonly", True)]},
        help="These should be delivered to every student in this training.")
    training_action_id = fields.Many2one(
        M % "action",
        "Training action",
        states={"done": [("readonly", True)]},
        help="Training action of this event, if it is a training group.")
    training_mode = fields.Boolean(
        compute="_compute_training_mode",
        help="Is the user using events in training mode?")

    @api.constrains("training_action_id")
    def _check_grade_limits(self):
        """Ensure no conflicts between limits and actual student grades."""
        self.registration_ids._check_grade_limits()

    @api.depends("name")
    def _compute_training_mode(self):
        """Know if the user is in the training menu.

        Field :attr:`~.training_mode` is used to know if the training action
        field should be required. It should if you use the *Training* menu, but
        not if you use the *Event* one.

        This does not really depend on :attr:`~.name`, but it needs to depend
        on something to make the UI trigger the calculation, and name is a
        required field that appears in every form, so it is a good candidate.
        """
        self.training_mode = bool(self.env.context.get("training_mode"))

    @api.onchange("training_action_id")
    def _fill_material_ids(self):
        """Autofill materials for this event."""
        for rec in self:
            if rec.training_action_id and not rec.material_ids:
                rec.material_ids = rec.training_action_id.material_ids
