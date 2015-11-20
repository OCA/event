# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import _, api, fields, models
from .. import exceptions as ex


class CourseType(models.Model):
    """Types of courses.

    Depending on the course type, a course may expect some
    type of hours. For example:

    - If a course's type is "on-site", it expects on-site hours.
    - If its type is "online", it expects online hours.
    - If its type is "mixed", it expects both on-site and online hours.
    """
    _name = "training.course_type"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(required=True, index=True, translate=True)
    course_ids = fields.One2many(
        "training.course",
        "type_id",
        "Courses",
        help="Courses of this type.")
    expected_duration_type_ids = fields.Many2many(
        "training.duration_type",
        string="Expected hour types",
        help="These types of hours are expected in this type of training "
             "course. For example, a training of type 'mixed' may expect "
             "hours of types 'on-site' and 'online'.")


class Course(models.Model):
    """Define courses.

    A course is one course that your company teaches and has in its
    catalog of courses.

    They define some requirements that the corresponding event is expected to
    fulfill. Events linked to courses are considered training groups.
    """
    _name = "training.course"

    name = fields.Char(required=True, index=True, translate=True)
    type_id = fields.Many2one(
        "training.course_type",
        "Training type",
        required=True)
    contents = fields.Html(
        translatable=True,
        help="Contents of the course, shown in the back side of the "
             "certificate.")
    contents_layout = fields.Selection(
        ((2, "2 columns"), (3, "3 columns"), (4, "4 columns")),
        help="Append one of these templates to the certificate contents. "
             "They will help you to achieve some complex layouts.")
    duration_ids = fields.One2many(
        "training.duration",
        "course_id",
        "Expected hours",
        copy=True,
        help="Expected duration of each type of hours for these training "
             "groups.")
    event_ids = fields.One2many("event.event", "course_id", "Events")
    grade_min = fields.Float(
        "Minimum grade",
        default=0,
        required=True,
        help="Students cannot get less than this grade.")
    grade_pass = fields.Float(
        "Passing grade",
        default=5,
        required=True,
        help="Students above this grade will pass the training.")
    grade_max = fields.Float(
        "Maximum grade",
        default=10,
        required=True,
        help="Students cannot get more than this grade.")
    product_ids = fields.Many2many(
        "product.product",
        string="Products",
        help="These should be delivered to every student in this training.")

    @api.constrains("grade_min", "grade_pass", "grade_max")
    def _check_grade_limits(self):
        """Ensure no conflicts with grade limits."""
        for s in self:
            # Grade limits must be coherent
            if not s.grade_min <= s.grade_pass <= s.grade_max:
                msg = (_("Minimum grade cannot be higher than maximum.")
                       if s.grade_min > s.grade_max
                       else _("Passing grade must be between minimum and "
                              "maximum grades."))
                raise ex.GradeLimitIncoherentError(msg)

            # Cannot conflict with existing student grades
            s.event_ids._check_grade_limits()

    @api.onchange("type_id")
    def _onchange_type_id_fulfill_expected_duration_types(self):
        """When choosing a type of course, fulfill the expected hours.

        There will be 0 hours of each type by default.
        """
        # Remove invalid hour expectations
        valid_duration_types = self.type_id.expected_duration_type_ids
        for duration in self.duration_ids:
            if duration.type_id not in valid_duration_types:
                self.duration_ids -= duration

        # Add new hour expectations
        current_duration_types = self.mapped("duration_ids.type_id")
        for duration_type in self.type_id.expected_duration_type_ids:
            if duration_type not in current_duration_types:
                new_duration = False

                # Try to restore it from DB
                if (self.env.context.get("active_model") == self._name and
                        self.env.context.get("active_id")):
                    new_duration = self.env["training.duration"].search((
                        ("type_id", "=", duration_type.id),
                        ("course_id", "=", self.env.context["active_id"]),
                    ))

                # Create a new one otherwise
                if not new_duration:
                    new_duration = self.duration_ids.new({
                        "course_id": self,
                        "type_id": duration_type,
                    })

                self.duration_ids |= new_duration

    @api.onchange("contents_layout")
    def _onchange_contents_layout(self):
        """Append the template to the contents and void that dummy field."""
        if self.contents_layout:
            single = '<div class="col-xs-{}">{}</div>'.format(
                12 / self.contents_layout,
                _("Column %d"))
            columns = range(1, self.contents_layout + 1)
            self.contents = (
                (self.contents or "") +
                ((single * self.contents_layout) % tuple(columns)))
            self.contents_layout = False
