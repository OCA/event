# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import api, fields, models
from .. import exceptions


class Registration(models.Model):
    """Allow to qualify a registration."""
    _inherit = "event.registration"

    grade = fields.Float(
        readonly=True,
        states={"done": [("readonly", False)]})
    materials_delivered = fields.Boolean(
        help="Training materials have been delivered to this student?")
    passing = fields.Boolean(
        compute="_compute_passing",
        help="Did the student pass the training?")
    training_action_id = fields.Many2one(
        related="event_id.training_action_id",
        string="Event's training action",
        readonly=True)

    @api.depends("grade", "event_id", "training_action_id",
                 "training_action_id.grade_pass")
    def _compute_passing(self):
        """Know if the student is passing the training."""
        for record in self:
            record.passing = (record.grade >=
                              record.training_action_id.grade_pass)

    @api.constrains("grade")
    def _check_grade_limits(self):
        """Ensure no conflicts between limits and actual student grades."""
        for record in self:
            if not (record.training_action_id.grade_min <=
                    record.grade <=
                    record.training_action_id.grade_max):
                raise exceptions.GradeLimitError(record)

    @api.constrains("materials_delivered")
    def _check_materials_delivered(self):
        """Cannot deliver materials if no materials are set."""
        for record in self:
            if self.materials_delivered and not record.event_id.material_ids:
                raise exceptions.NoMaterialsToDeliverError()
