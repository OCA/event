# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from typing import List

import pydantic

from odoo.addons.pydantic import models, utils

from .event_stage_info import EventStageInfo
from .event_ticket_info import EventTicketInfo
from .event_type_info import EventTypeInfo


class EventShortInfo(models.BaseModel):
    id: int
    name: str
    date_begin: datetime
    date_end: datetime
    event_type: EventTypeInfo = pydantic.Field(None, alias="event_type_id")
    stage: EventStageInfo = pydantic.Field(None, alias="stage_id")
    write_date: datetime

    class Config:
        orm_mode = True
        getter_dict = utils.GenericOdooGetter


class EventInfo(EventShortInfo):
    event_tickets: List[EventTicketInfo] = pydantic.Field([], alias="event_ticket_ids")
