# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class EventRegistrationCancelLogReason(models.TransientModel):
    _name = 'event.registration.cancel.log.reason'

    event_id = fields.Many2one(comodel_name="event.event", string="Event")
    reason_id = fields.Many2one(
        comodel_name="event.registration.cancel.reason", required=True,
        domain="['|', "
               " ('event_ids', '=', False), "
               " ('event_ids', '=', event_id)]")

    @api.model
    def default_get(self, var_fields):
        res = super(EventRegistrationCancelLogReason, self).default_get(
            var_fields)
        registration = self.env['event.registration'].browse(
            self.env.context['active_id'])
        res['event_id'] = registration.event_id.id
        return res

    @api.multi
    def button_log(self):
        self.ensure_one()
        registration = self.env['event.registration'].browse(
            self.env.context['active_id'])
        registration.cancel_reason_id = self.reason_id.id
        registration.with_context(bypass_reason=True).button_reg_cancel()
