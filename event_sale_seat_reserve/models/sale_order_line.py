# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
import logging

from odoo import models
from odoo.tools import config

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _update_registrations(
        self,
        confirm=True,
        cancel_to_draft=False,
        registration_data=None,
        mark_as_paid=False,
    ):
        res = super(SaleOrderLine, self)._update_registrations(
            confirm=confirm,
            cancel_to_draft=cancel_to_draft,
            registration_data=registration_data,
            mark_as_paid=mark_as_paid,
        )
        RegistrationSudo = self.env["event.registration"].sudo()
        registrations = RegistrationSudo.search(
            [("sale_order_line_id", "in", self.ids), ("state", "=", "draft")]
        )
        if config["test_enable"] and not self.env.context.get(
            "test_event_seat_reserve"
        ):
            _logger.info("Test mode is enabled, skipping the reservation of the seats")
            return res
        registrations.action_set_reserved()
        return res

    def _set_draft_associated_registrations(self):
        RegistrationSudo = self.env["event.registration"].sudo()
        registrations = RegistrationSudo.search(
            [("sale_order_line_id", "in", self.ids), ("state", "!=", "done")]
        )
        registrations.action_set_draft()
        return True
