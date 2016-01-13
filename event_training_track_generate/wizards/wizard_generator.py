# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import _, api, exceptions, fields, models


class Generator(models.TransientModel):
    _inherit = "event.track.generator"

    is_training = fields.Boolean(
        readonly=True,
        related="event_id.is_training")
    duration_type_id = fields.Many2one(
        "event.training.duration.type",
        "Training duration type",
        help="Training duration type of generated tracks.")
    stop_when_reaching_expected_durations = fields.Boolean(
        default=True,
        help="Only generate enough tracks to fulfill the expected hours of "
             "the chosen type.")

    @api.multi
    @api.onchange("is_training")
    def _onchange_event_change_durations_domain(self):
        """Change the domain for ``duration_type_id`` as needed."""
        if self.is_training:
            types = (self.event_id.type.expected_duration_type_ids |
                     self.event_id.product_id.mapped("duration_ids.type_id"))
            return {
                "domain": {
                    "duration_type_id": [
                        ("id", "in", types.ids),
                    ],
                },
            }

    @api.multi
    def create_track(self, **values):
        """Create tracks with duration type.

        In case the expected durations are already reached, this will generate
        nothing.

        In case the generated track would overflow the expectations, its
        duration will be automatically trimmed.
        """
        if self.is_training and self.duration_type_id:
            values.setdefault("duration_type_id", self.duration_type_id.id)
            if self.stop_when_reaching_expected_durations:
                # Compare current duration with the expected one
                current = sum(
                    self.event_id.track_ids
                    .filtered(
                        lambda r: r.duration_type_id == self.duration_type_id)
                    .mapped("duration"))
                expected = self.event_id.product_id.duration_ids.filtered(
                    lambda r: r.type_id == self.duration_type_id).duration

                if not expected:
                    raise exceptions.ValidationError(
                        _("No expected duration set for type %s.") %
                        self.duration_type_id.display_name)
                elif current >= expected:
                    # Do not generate; return empty record
                    return self.env["event.track"]
                elif current + self.duration > expected:
                    # Trim next generated track duration
                    values["duration"] = expected - current

        # Fall back to original method
        return super(Generator, self).create_track(**values)
