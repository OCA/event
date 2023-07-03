# Copyright 2023 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import http

from odoo.addons.website_event_sale_joined_constraint.controllers.website_event_sale_joined_constraint_controller import (  # noqa: B950
    WebsiteEventSaleJoinedConstraintController,
)
from odoo.addons.website_event_sale_single_attendee.controllers.main import (
    WebsiteEventSaleControllerSingleAttendee,
)


class WebsiteEventSaleJoinedConstraintControllerSingleAttendee(
    WebsiteEventSaleControllerSingleAttendee, WebsiteEventSaleJoinedConstraintController
):
    @http.route()
    def registration_new(self, event, **post):
        tickets = self._process_tickets_form(event, post)
        if self._only_child_tickets_sold(tickets):
            return False
        return super(WebsiteEventSaleControllerSingleAttendee, self).registration_new(
            event, **post
        )
