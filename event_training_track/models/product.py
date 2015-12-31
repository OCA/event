# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import api, fields, models


class EventTrainingProductABC(models.AbstractModel):
    _name = "event_training_track.product_abc"

    @api.multi
    @api.onchange("event_type_id", "is_training")
    def _onchange_event_type_id_fill_duration_ids(self):
        """When choosing a training type, fulfill the durations."""
        (self.filtered(lambda r: r.is_training and not r.duration_ids)
         .action_fill_duration_ids())

    @api.multi
    def action_fill_duration_ids(self):
        """Fill :attr:`duration_ids` with the expected types."""
        # Creation of durations should work in onchange and outside it
        new_duration = getattr(
            self.env["event.training.duration"],
            "new" if self.env.in_onchange else "create")

        for s in self:
            # Remove invalid durations
            expected_types = s.event_type_id.expected_duration_type_ids
            s.duration_ids.filtered(
                lambda r: r.type_id not in expected_types).unlink()

            # Add new hour expectations
            product = getattr(s, "product_tmpl_id", s)
            current_types = s.mapped("duration_ids.type_id")
            for missing_type in expected_types - current_types:
                s.duration_ids |= new_duration({
                    "product_tmpl_id": product.id,
                    "type_id": missing_type.id,
                })


class ProductTemplate(models.Model):
    """Manage durations per product template."""
    _name = "product.template"
    _inherit = ["product.template", "event_training_track.product_abc"]

    duration_ids = fields.One2many(
        "event.training.duration",
        "product_tmpl_id",
        "Expected durations",
        copy=True,
        help="Expected duration per hour type for these events.")


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "event_training_track.product_abc"]
