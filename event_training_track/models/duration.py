# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import _, api, fields, models


class EventTrainingDurationType(models.Model):
    """Types of the courses' durations."""
    _name = "event.training.duration.type"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(
        index=True,
        required=True,
        translate=True)
    monitor_attendance = fields.Boolean(
        help="Does this hour type use attendance monitoring?")
    duration_ids = fields.One2many(
        "event.training.duration",
        "type_id",
        "Durations",
        help="Durations found of this type.")

    @api.multi
    def copy(self, default=None):
        """Avoid unique key failure when copying."""
        default = default or dict()
        default.setdefault("name", _("%s (copy)") % self.name)
        return super(EventTrainingDurationType, self).copy(default)


class EventTrainingDuration(models.Model):
    """Durations expected for each training event product."""
    _name = "event.training.duration"
    _rec_name = "duration"
    _sql_constraints = [("type_vs_product",
                         "UNIQUE(type_id, product_tmpl_id)",
                         "Cannot repeat the hour type in a product.")]

    duration = fields.Float(
        default=0,
        required=True)
    type_id = fields.Many2one(
        "event.training.duration.type",
        "Type",
        required=True,
        help="Hour type.")
    product_tmpl_id = fields.Many2one(
        "product.template",
        "Product",
        ondelete="cascade",
        required=True,
        help="Training event product that expects this duration.")
