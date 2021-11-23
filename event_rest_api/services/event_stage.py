# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import List

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_pydantic.restapi import PydanticModel, PydanticModelList
from odoo.addons.component.core import Component

from ..pydantic_models.event_stage_info import EventStageInfo
from ..pydantic_models.event_stage_search_filter import EventStageSearchFilter


class EventStageService(Component):
    _inherit = "base.event.rest.service"
    _name = "event.stage.rest.service"
    _usage = "event_stage"
    _expose_model = "event.stage"
    _description = __doc__

    @restapi.method(
        routes=[(["/<int:_id>"], "GET")],
        output_param=PydanticModel(EventStageInfo),
        auth="public",
    )
    def get(self, _id: int) -> EventStageInfo:
        event_stage = self._get(_id)
        return EventStageInfo.from_orm(event_stage)

    def _get_search_domain(self, filters):
        domain = []
        if filters.name:
            domain.append(("name", "like", filters.name))
        if filters.id:
            domain.append(("id", "=", filters.id))
        if filters.pipe_end is not None:
            domain.append(("pipe_end", "=", filters.pipe_end))
        return domain

    @restapi.method(
        routes=[(["/", "/search"], "GET")],
        input_param=PydanticModel(EventStageSearchFilter),
        output_param=PydanticModelList(EventStageInfo),
        auth="public",
    )
    def search(
        self, event_stage_search_filter: EventStageSearchFilter
    ) -> List[EventStageInfo]:
        domain = self._get_search_domain(event_stage_search_filter)
        res: List[EventStageInfo] = []
        for e in self.env["event.stage"].sudo().search(domain):
            res.append(EventStageInfo.from_orm(e))
        return res
