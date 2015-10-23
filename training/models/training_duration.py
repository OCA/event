# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import api, fields, models
from .common import M
from .. import exceptions


class DurationType(models.Model):
    """Types of the training actions' durations.

    See docs for :class:`~.ActionType`.
    """

    _name = M % "duration_type"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(required=True, index=True, translate=True)
    duration_ids = fields.One2many(
        M % "duration",
        "type_id",
        "Expected hours of this type",
        help="Expected hours of this type defined in training actions.")
    action_type_ids = fields.Many2many(
        M % "action_type",
        string="Training action types",
        help="Training action types that expect this hour type.")


class Duration(models.Model):
    _name = M % "duration"
    _sql_constraints = [("training_vs_hours_unique",
                         "UNIQUE(type_id, action_id)",
                         "Cannot repeat the hour type in a training action.")]

    duration = fields.Float(default=0, required=True)
    type_id = fields.Many2one(
        M % "duration_type",
        "Type of hours",
        required=True)
    action_id = fields.Many2one(
        M % "action",
        "Training action",
        required=True)

    @api.multi
    @api.constrains("type_id", "action_id")
    def _check_right_duration_types(self):
        """Check that the hour types are the right ones."""

        expected_types = (self.action_id.type_id
                          .expected_duration_type_ids)

        if expected_types and self.type_id not in expected_types:
            raise exceptions.WrongDurationTypeError(
                self.type_id,
                expected_types)
