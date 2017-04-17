# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import api, fields, models
from .. import exceptions


class Event(models.Model):
    """Expand events with courses.

    Events with a training type and a course are considered training
    groups.
    """
    _inherit = "event.event"

    product_ids = fields.Many2many(
        "product.product",
        string="Products",
        states={"done": [("readonly", True)]},
        help="These should be delivered to every student in this training.")
    course_id = fields.Many2one(
        "training.course",
        "Course",
        states={"done": [("readonly", True)]},
        help="Course of this event, if it is a training group.")
    training_mode = fields.Boolean(
        compute="_compute_training_mode",
        help="Is the user using events in training mode?")

    @api.constrains("course_id")
    def _check_grade_limits(self):
        """Ensure no conflicts between limits and actual student grades."""
        self.registration_ids._check_grade_limits()

    @api.onchange("product_ids")
    def _onchange_product_ids_check_delivered(self):
        """Warn if any products have already been delivered."""
        if any(self.mapped("registration_ids.products_delivered")):
            raise exceptions.ChangeDeliveredProductsWarning()

    @api.depends("name")
    def _compute_training_mode(self):
        """Know if the user is in the training menu.

        Field :attr:`~.training_mode` is used to know if the course
        field should be required. It should if you use the *Training* menu, but
        not if you use the *Event* one.

        This does not really depend on :attr:`~.name`, but it needs to depend
        on something to make the UI trigger the calculation, and name is a
        required field that appears in every form, so it is a good candidate.
        """
        self.training_mode = bool(self.env.context.get("training_mode"))

    @api.onchange("course_id")
    def _fill_product_ids(self):
        """Autofill products for this event."""
        for rec in self:
            if rec.course_id and not rec.product_ids:
                rec.product_ids = rec.course_id.product_ids
