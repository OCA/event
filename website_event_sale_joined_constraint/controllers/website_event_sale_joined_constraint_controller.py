# Copyright 2023 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import http

from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController


class WebsiteEventSaleJoinedConstraintController(WebsiteEventSaleController):
    @http.route()
    def registration_new(self, event, **post):
        tickets = self._process_tickets_form(event, post)
        if self._only_child_tickets_sold(tickets):
            return False
        return super().registration_new(event, **post)

    def _process_tickets_form(self, event, form_details):
        """Add constraints information on ticket order"""
        res = super(WebsiteEventSaleController, self)._process_tickets_form(
            event, form_details
        )
        for item in res:
            item["is_child"] = (
                item["ticket"]["is_child_ticket"] if item["ticket"] else False
            )
        return res

    def _only_child_tickets_sold(self, tickets):
        return all([ticket["is_child"] for ticket in tickets])
