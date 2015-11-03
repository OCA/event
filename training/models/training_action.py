# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import _, api, fields, models
from .common import M
from .. import exceptions as ex


class ActionType(models.Model):
    """Types of training actions.

    Depending on the training action type, a training action may expect some
    type of hours. For example:

    - If a training action's type is "on-site", it expects on-site hours.
    - If its type is "online", it expects online hours.
    - If its type is "mixed", it expects both on-site and online hours.

    You can configure it as you wish.
    """
    _name = M % "action_type"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(required=True, index=True, translate=True)
    action_ids = fields.One2many(
        M % "action",
        "type_id",
        "Training actions",
        help="Training actions of this type.")
    expected_duration_type_ids = fields.Many2many(
        M % "duration_type",
        string="Expected hour types",
        help="These types of hours are expected in this type of training "
             "action. For example, a training of type 'mixed' may expect "
             "hours of types 'on-site' and 'online'.")


class Action(models.Model):
    """Define training actions.

    A training action is one course that your company teaches and has in its
    catalog of courses.

    They define some requirements that the corresponding event is expected to
    fulfill. Events linked to training actions are considered training groups.
    """
    _name = M % "action"

    name = fields.Char(required=True, index=True, translate=True)
    type_id = fields.Many2one(
        M % "action_type",
        "Training type",
        required=True)
    contents = fields.Html(
        translatable=True,
        help="Contents of the course, shown in the rear side of the diploma.")
    append_template = fields.Selection(
        ((2, "2 columns"), (3, "3 columns"), (4, "4 columns")),
        help="Append one of these templates to the diploma contents. "
             "They will help you to achieve some complex layouts.")
    duration_ids = fields.One2many(
        M % "duration",
        "action_id",
        "Expected hours",
        copy=True,
        help="Expected duration of each type of hours for these training "
             "groups.")
    event_ids = fields.One2many("event.event", "training_action_id", "Events")
    grade_min = fields.Float(
        "Minimal grade",
        default=0,
        required=True,
        help="Students cannot get less than this grade.")
    grade_pass = fields.Float(
        "Passing grade",
        default=5,
        required=True,
        help="Students above than this grade will pass the training.")
    grade_max = fields.Float(
        "Maximum grade",
        default=10,
        required=True,
        help="Students cannot get more than this grade.")

    @api.constrains("grade_min", "grade_pass", "grade_max")
    def _check_grade_limits(self):
        """Ensure no conflicts with grade limits."""
        for s in self:
            # Grade limits must be coherent
            if not s.grade_min <= s.grade_pass <= s.grade_max:
                msg = (_("Minimum grade cannot be bigger than maximum.")
                       if s.grade_min > s.grade_max
                       else _("Passing grade must be between minimum and "
                              "maximum grades."))
                raise ex.GradeLimitIncoherentError(msg)

            # Cannot conflict with existing student grades
            s.event_ids._check_grade_limits()

    @api.onchange("type_id")
    def _onchange_type_id_fulfill_expected_duration_types(self):
        """When choosing a type of training action, fulfill the expected hours.

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
                    new_duration = self.env[M % "duration"].search((
                        ("type_id", "=", duration_type.id),
                        ("action_id", "=", self.env.context["active_id"]),
                    ))

                # Create a new one otherwise
                if not new_duration:
                    new_duration = self.duration_ids.new({
                        "action_id": self,
                        "type_id": duration_type,
                    })

                self.duration_ids |= new_duration

    @api.onchange("append_template")
    def _onchange_append_template(self):
        """Append the template to the contents and void that dummy field."""
        if self.append_template:
            single = '<div class="col-xs-{}">{}</div>'.format(
                12 / self.append_template,
                _("Column %d"))
            columns = range(1, self.append_template + 1)
            self.contents += (single * self.append_template) % tuple(columns)
            self.append_template = False
