# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _need_pre_reservation(self):
        need_pre_reservation = super()._need_pre_reservation()

        return need_pre_reservation and self.visitor_id

    @api.model_create_multi
    def create(self, vals_list):
        registrations = super(EventRegistration, self).create(vals_list)
        for registration in registrations:
            if registration._need_pre_reservation():
                registration.action_set_reserved()
        return registrations
