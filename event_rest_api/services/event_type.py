# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import List

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_pydantic.restapi import PydanticModel, PydanticModelList
from odoo.addons.component.core import Component

from ..pydantic_models.event_type_info import EventTypeInfo
from ..pydantic_models.event_type_search_filter import EventTypeSearchFilter


class EventTypeService(Component):
    _inherit = "base.event.rest.service"
    _name = "event.type.rest.service"
    _usage = "event_type"
    _expose_model = "event.type"
    _description = __doc__

    @restapi.method(
        routes=[(["/<int:_id>"], "GET")],
        output_param=PydanticModel(EventTypeInfo),
        auth="public",
    )
    def get(self, _id: int) -> EventTypeInfo:
        event_type = self._get(_id)
        return EventTypeInfo.from_orm(event_type)

    def _get_search_domain(self, filters):
        domain = []
        if filters.name:
            domain.append(("name", "like", filters.name))
        if filters.id:
            domain.append(("id", "=", filters.id))
        return domain

    @restapi.method(
        routes=[(["/", "/search"], "GET")],
        input_param=PydanticModel(EventTypeSearchFilter),
        output_param=PydanticModelList(EventTypeInfo),
        auth="public",
    )
    def search(
        self, event_type_search_filter: EventTypeSearchFilter
    ) -> List[EventTypeInfo]:
        domain = self._get_search_domain(event_type_search_filter)
        res: List[EventTypeInfo] = []
        for e in self.env["event.type"].sudo().search(domain):
            res.append(EventTypeInfo.from_orm(e))
        return res
