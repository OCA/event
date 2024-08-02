# Copyright 2016 Antiun Ingeniería S.L.
# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Cristina Martin
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    cancel_reason_id = fields.Many2one(
        comodel_name='event.registration.cancel.reason', readonly=True,
        string="Cancellation Reason", ondelete="restrict")

    @api.multi
    def button_reg_cancel(self):
        if self.env.context.get('bypass_reason'):
            return super(EventRegistration, self).button_reg_cancel()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancellation reason',
            'res_model': 'event.registration.cancel.log.reason',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def do_draft(self):
        super(EventRegistration, self).do_draft()
        self.write({'cancel_reason_id': False})


class EventRegistrationCancelReason(models.Model):
    _name = 'event.registration.cancel.reason'
    _description = 'Event Registration Cancel Reason'

    name = fields.Char('Reason', required=True, translate=True)
    event_type_ids = fields.Many2many(
        comodel_name="event.type", string="Event types",
        help="Select the event types where you want to use this cancellation "
             "reason. Leave it empty for using in all.")
