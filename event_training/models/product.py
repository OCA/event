# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import _, api, fields, models
from .. import exceptions as ex


class EventTrainingBase(models.Model):
    """Shared logic between template and product."""
    _name = "event_training.base"

    @api.multi
    @api.constrains("grade_min", "grade_pass", "grade_max")
    def _check_grade_limits(self):
        """Ensure no conflicts with grade limits."""
        for s in self:
            # Grade limits must be coherent
            if not s.grade_min <= s.grade_pass <= s.grade_max:
                if s.grade_min > s.grade_max:
                    raise ex.GradeLimitOverflowError(s)
                else:
                    raise ex.GradePassingOverflowError(s)

            # Cannot conflict with existing student grades
            s.mapped("product_variant_ids.event_ids")._check_grade_limits()

    @api.multi
    @api.onchange("contents_layout")
    def _onchange_contents_layout(self):
        """Append the template to the contents and void that dummy field."""
        for s in self:
            if s.contents_layout:
                single = '<div class="col-xs-{}">{}</div>'.format(
                    12 / s.contents_layout,
                    _("Column %d"))
                columns = range(1, s.contents_layout + 1)
                s.contents = (
                    (s.contents or "") +
                    ((single * s.contents_layout) % tuple(columns)))
                s.contents_layout = False


class ProductTemplate(models.Model):
    """Expand event products for training needs. Now products define courses.

    They define some requirements that the corresponding event is expected to
    fulfill. Events linked to courses are considered training events.
    """
    _name = "product.template"
    _inherit = ["product.template", "event_training.base"]

    is_training = fields.Boolean(
        "Is a course",
        related="event_type_id.is_training",
        readonly=True,
        help="Does the chosen event type make this product a course?")
    contents = fields.Html(
        translatable=True,
        help="Contents of the course, shown in the back side of the "
             "certificate.")
    contents_layout = fields.Selection(
        ((2, "2 columns"), (3, "3 columns"), (4, "4 columns")),
        help="Append one of these templates to the certificate contents. "
             "They will help you to achieve some complex layouts.")
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


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "event_training.base"]
