# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import api, fields, models


class Generator(models.TransientModel):
    _inherit = "event_track_generate.generator"

    available_duration_type_ids = fields.Many2many(
        "training.duration_type",
        compute="_compute_available_duration_type_ids",
        store=True)
    duration_type_id = fields.Many2one(
        "training.duration_type",
        "Training hour type",
        domain="[('id', 'in', available_duration_type_ids[0][2])]",
        help="Training hour type of generated tracks, if they belong to a "
             "training group.")
    event_is_training = fields.Boolean(
        compute="_compute_event_is_training",
        store=True)

    @api.one
    @api.depends("event_id")
    def _compute_available_duration_type_ids(self):
        """Get the list of available duration types.

        This list is a :class:`~fields.Many2many`, which in the client side
        has a value like ``[6, False, [<list-of-ids>]]``, that's why
        :attr:`.duration_type_id` has that weird domain.
        """
        self.available_duration_type_ids = self.event_id.mapped(
            'training_action_id.duration_ids.type_id')

    @api.one
    @api.depends("event_id")
    def _compute_event_is_training(self):
        """Know if the related event is a training group."""
        self.event_is_training = bool(self.event_id.training_action_id)

    @api.one
    def create_track(self, **values):
        """Create tracks with duration type."""
        values.setdefault("duration_type_id", self.duration_type_id.id)
        super(Generator, self).create_track(**values)
