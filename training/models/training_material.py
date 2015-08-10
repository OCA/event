# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import fields, models
from .common import M


class MaterialType(models.Model):
    """Type of the training materials."""
    _name = M % "material_type"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(required=True, index=True, translate=True)
    material_ids = fields.One2many(
        M % "material",
        "type_id",
        string="Materials",
        help="Available materials of this type.")


class Material(models.Model):
    """Training material delivered to students."""
    _name = M % "material"
    _sql_constraints = [("unique_name",
                         "UNIQUE(name)",
                         "Name must be unique.")]

    name = fields.Char(required=True, index=True, translate=True)
    type_id = fields.Many2one(
        M % "material_type",
        "Type",
        ondelete="restrict",
        help="Type of this training material")
    event_ids = fields.Many2many(
        "event.event",
        string="Events",
        help="This material should be delivered in these training groups.")
    course_ids = fields.Many2many(
        M % "course",
        string="Courses",
        help="This material should be delivered in these courses.")
