# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import api, fields, models
from . import exceptions


# Current module domain
_D = "training.%s"


class DurationType(models.Model):
    """Types of the training actions' durations.

    See docs for :class:`~.ActionType`.
    """

    _name = _D % "duration_type"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(required=True, index=True, translate=True)
    duration_ids = fields.One2many(
        _D % "duration",
        "type_id",
        "Expected hours of this type",
        help="Expected hours of this type defined in training actions.")
    action_type_ids = fields.Many2many(
        _D % "action_type",
        string="Training action types",
        help="Training action types that expect this hour type.")


class Duration(models.Model):
    _name = _D % "duration"
    _sql_constraints = [("training_vs_hours_unique",
                         "UNIQUE(type_id, action_id)",
                         "Cannot repeat the hour type in a training action.")]

    duration = fields.Float(default=0, required=True)
    type_id = fields.Many2one(
        _D % "duration_type",
        "Type of hours",
        required=True)
    action_id = fields.Many2one(
        _D % "action",
        "Training action",
        required=True)

    @api.multi
    @api.constrains("type_id", "action_id")
    def _check_right_duration_types(self):
        """Check that the hour types are the right ones."""

        expected_types = (self.action_id.type_id
                          .expected_duration_type_ids)

        if expected_types and self.type_id not in expected_types:
            raise exceptions.WrongDurationType(
                self.type_id,
                expected_types)


class ActionType(models.Model):
    """Types of training actions.

    Depending on the training action type, a training action may expect some
    type of hours. For example:

    - If a training action's type is "on-site", it expects on-site hours.
    - If its type is "online", it expects online hours.
    - If its type is "mixed", it expects both on-site and online hours.

    You can configure it as you wish.
    """

    _name = _D % "action_type"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(required=True, index=True, translate=True)
    action_ids = fields.One2many(
        _D % "action",
        "type_id",
        "Training actions",
        help="Training actions of this type.")
    expected_duration_type_ids = fields.Many2many(
        _D % "duration_type",
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

    _name = _D % "action"

    name = fields.Char(required=True, index=True, translate=True)
    type_id = fields.Many2one(
        _D % "action_type",
        "Training type",
        required=True)
    contents = fields.Html(
        help="Contents of the course, shown in the rear side of the diploma.")
    duration_ids = fields.One2many(
        _D % "duration",
        "action_id",
        "Expected hours",
        help="Expected duration of each type of hours for these training "
             "groups.")
    event_ids = fields.One2many("event.event", "training_action_id", "Events")

    @api.onchange("type_id")
    def _onchange_type_id_fulfill_expected_duration_types(self):
        """When choosing a type of training action, fulfill the expected hours.

        There will be 0 hours of each type by default.
        """

        # Remove invalid hour expectations
        valid_duration_types = self.type_id.expected_duration_type_ids
        for duration in self.duration_ids:
            if duration.duration_type_id not in valid_duration_types:
                self.duration_ids -= duration

        # Add new hour expectations
        current_duration_types = self.mapped("duration_ids.type_id")
        for duration_type in self.type_id.expected_duration_type_ids:
            if duration_type not in current_duration_types:
                self.duration_ids |= self.duration_ids.new(
                    {"action_id": self,
                     "type_id": duration_type})


class Event(models.Model):
    """Expand events with training actions.

    Events with a training type and a training action are considered training
    groups.
    """

    _inherit = "event.event"

    training_action_id = fields.Many2one(
        _D % "action",
        "Training action",
        help="Training action of this event, if it is a training group.")
