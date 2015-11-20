# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import api, fields, models
from .. import exceptions


class DurationType(models.Model):
    """Types of the courses' durations.

    See docs for :class:`~.CourseType`.
    """
    _name = "training.duration_type"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(required=True, index=True, translate=True)
    duration_ids = fields.One2many(
        "training.duration",
        "type_id",
        "Expected hours of this type",
        help="Expected hours of this type defined in courses.")
    course_type_ids = fields.Many2many(
        "training.course_type",
        string="Course types",
        help="Course types that expect this hour type.")


class Duration(models.Model):
    """Durations expected for each course."""
    _name = "training.duration"
    _sql_constraints = [("training_vs_hours_unique",
                         "UNIQUE(type_id, course_id)",
                         "Cannot repeat the hour type in a course.")]

    duration = fields.Float(default=0, required=True)
    type_id = fields.Many2one(
        "training.duration_type",
        "Type of hours",
        required=True)
    course_id = fields.Many2one(
        "training.course",
        "Course",
        ondelete="cascade",
        required=True)

    @api.multi
    @api.constrains("type_id", "course_id")
    def _check_right_duration_types(self):
        """Check that the hour types are the right ones."""
        for rec in self:
            expected_types = (rec.course_id.type_id
                              .expected_duration_type_ids)

            if expected_types and rec.type_id not in expected_types:
                raise exceptions.WrongDurationTypeError(
                    rec.type_id,
                    expected_types)
