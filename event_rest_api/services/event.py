# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import List

from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_pydantic.restapi import PydanticModel, PydanticModelList
from odoo.addons.component.core import Component

from ..pydantic_models.event_info import EventInfo
from ..pydantic_models.event_registration_info import EventRegistrationInfo
from ..pydantic_models.event_registration_request import (
    EventRegistrationRequest,
    EventRegistrationRequestList,
)
from ..pydantic_models.event_search_filter import EventSearchFilter


class EventService(Component):
    _inherit = "base.event.rest.service"
    _name = "event.rest.service"
    _usage = "event"
    _expose_model = "event.event"
    _description = __doc__

    @restapi.method(
        routes=[(["/<int:_id>"], "GET")],
        output_param=PydanticModel(EventInfo),
        auth="public",
    )
    def get(self, _id: int) -> EventInfo:
        event = self._get(_id)
        return EventInfo.from_orm(event)

    def _get_search_domain(self, filters):
        domain = []
        if filters.name:
            domain.append(("name", "like", filters.name))
        if filters.id:
            domain.append(("id", "=", filters.id))
        if filters.start_after:
            domain.append(("date_begin", ">", filters.start_after))
        if filters.end_before:
            domain.append(("date_end", "<", filters.end_before))
        if filters.event_type_ids:
            domain.append(("event_type_id", "in", filters.event_type_ids))
        if filters.stage_ids:
            domain.append(("stage_id", "in", filters.stage_ids))
        return domain

    @restapi.method(
        routes=[(["/", "/search"], "GET")],
        input_param=PydanticModel(EventSearchFilter),
        output_param=PydanticModelList(EventInfo),
        auth="public",
    )
    def search(self, event_search_filter: EventSearchFilter) -> List[EventInfo]:
        domain = self._get_search_domain(event_search_filter)
        res: List[EventInfo] = []
        for e in self.env["event.event"].sudo().search(domain):
            res.append(EventInfo.from_orm(e))
        return res

    def _prepare_event_registration_values(
        self, event, event_registration_request: EventRegistrationRequest
    ) -> dict:
        return {
            "event_id": event.id,
            "partner_id": self.env.context.get("authenticated_partner_id", False),
            "firstname": event_registration_request.firstname,
            "lastname": event_registration_request.lastname,
            "email": event_registration_request.email,
            "phone": event_registration_request.phone,
            "event_ticket_id": event_registration_request.event_ticket_id,
        }

    @restapi.method(
        routes=[(["/<int:_id>/registration"], "POST")],
        input_param=PydanticModel(EventRegistrationRequestList),
        output_param=PydanticModelList(EventRegistrationInfo),
        auth="public_or_default",
    )
    def registration(
        self, _id: int, event_registration_request_list: EventRegistrationRequestList
    ) -> List[EventRegistrationInfo]:
        event = self._get(_id)
        if event.seats_limited:
            ordered_seats = len(
                event_registration_request_list.event_registration_requests
            )
            if event.seats_available < ordered_seats:
                raise ValidationError(
                    _("Not enough seats available: %s") % (event.seats_available)
                )
        res: List[EventRegistrationInfo] = []
        for (
            event_registration_request
        ) in event_registration_request_list.event_registration_requests:
            event_registration_values = self._prepare_event_registration_values(
                event, event_registration_request
            )
            event_registration = self.env["event.registration"].create(
                event_registration_values
            )
            res.append(EventRegistrationInfo.from_orm(event_registration))
        return res
