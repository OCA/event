# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class EventTrainingDurationSummary(models.TransientModel):
    _name = "event.training.duration.summary"
    _description = "Compare all the expected durations with the real ones"

    event_id = fields.Many2one(
        "event.event",
        "Event",
        readonly=True,
        default=lambda self: self.env.context["active_id"])
    line_ids = fields.One2many(
        "event.training.duration.summary.line",
        "summary_id",
        "Lines",
        readonly=True)

    @api.multi
    @api.onchange("event_id")
    def _load_lines(self):
        """Load lines for the event."""
        self.line_ids.unlink()
        types = (self.event_id.type.expected_duration_type_ids |
                 self.mapped("event_id.track_ids.duration_type_id"))
        for t in types:
            self.line_ids |= self.line_ids.new({
                "summary_id": self.id,
                "duration_type_id": t.id,
            })


class EventTrainingDurationSummaryLine(models.TransientModel):
    _name = "event.training.duration.summary.line"
    _description = "Compare one expected duration with the real ones"

    summary_id = fields.Many2one(
        "event.training.duration.summary",
        "Summary",
        required=True)
    duration_type_id = fields.Many2one(
        "event.training.duration.type",
        "Type",
        required=True)
    monitor_attendance = fields.Boolean(
        related="duration_type_id.monitor_attendance")
    expected_hours = fields.Float(
        compute="_compute_duration",
        help="Expected hours of this type for this event.")
    real_hours = fields.Float(
        compute="_compute_duration",
        help="Actual hours of this type for this event.")
    remaining_hours = fields.Float(
        compute="_compute_duration",
        help="How many hours are remaining to fulfill the expected ones?")

    @api.multi
    @api.depends("summary_id", "duration_type_id")
    def _compute_duration(self):
        """Get expected and real durations."""
        for s in self:
            s.expected_hours = self.env["event.training.duration"].search([
                ("type_id", "=", s.duration_type_id.id),
                ("product_tmpl_id", "=",
                 s.summary_id.event_id.product_id.product_tmpl_id.id),
            ]).duration
            s.real_hours = sum(
                self.env["event.track"].search([
                    ("event_id", "=", s.summary_id.event_id.id),
                    ("duration_type_id", "=", s.duration_type_id.id),
                ])
                .mapped("duration"))
            s.remaining_hours = s.expected_hours - s.real_hours
