# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    registrations = fields.One2many(
        string="Event registrations",
        comodel_name='event.registration', inverse_name="partner_id")
    event_count = fields.Integer(
        string='Events',
        compute='_compute_event_count',
        help="Count of events with confirmed registrations.",
    )

    @api.one
    @api.depends('registrations.state')
    def _compute_event_count(self):
        self.event_count = len(
            self.env["event.registration"].search([
                ("partner_id", "child_of", self.id),
                ("state", "not in", ("cancel", "draft")),
            ]).mapped("event_id"))
