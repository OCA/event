# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import api, fields, models
from .. import exceptions


class EventEvent(models.Model):
    """Expand events with courses.

    Events with a training type and a course are considered training
    groups.
    """
    _inherit = "event.event"

    is_training = fields.Boolean(
        related="type.is_training",
        readonly=True,
        help="Is this a training event?")

    @api.multi
    @api.constrains("product_id")
    def _check_grade_limits(self):
        """Ensure no conflicts between limits and actual student grades."""
        self.mapped("registration_ids")._check_grade_limits()


class EventRegistration(models.Model):
    """Allow the qualification of a registration."""
    _inherit = "event.registration"

    is_training = fields.Boolean(
        related="event_id.is_training",
        readonly=True,
        help="Is this a training registration?")
    grade = fields.Float(
        readonly=True,
        states={"done": [("readonly", False)]})
    passing = fields.Boolean(
        compute="_compute_passing",
        help="Did the student pass the training?")

    @api.multi
    @api.depends("grade", "event_id", "event_id.product_id.grade_pass")
    def _compute_passing(self):
        """Know if the student is passing the training."""
        for s in self:
            s.passing = s.grade >= s.event_id.product_id.grade_pass

    @api.multi
    @api.constrains("grade",
                    "is_training",
                    "event_id.product_id.grade_min",
                    "event_id.product_id.grade_max")
    def _check_grade_limits(self):
        """Ensure no conflicts between limits and actual student grades."""
        for s in self.filtered("is_training"):
            product = s.event_id.product_id
            if not product.grade_min <= s.grade <= product.grade_max:
                raise exceptions.StudentGradeOutsideLimitsError(
                    grade=s.grade,
                    student=s.name,
                    min=s.event_id.product_id.grade_min,
                    max=s.event_id.product_id.grade_max)


class EventType(models.Model):
    """Know which event types are for training courses."""
    _inherit = "event.type"

    is_training = fields.Boolean(
        help="Events and products of this type are courses.")
