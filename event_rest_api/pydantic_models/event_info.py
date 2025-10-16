# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from typing import List

import pydantic
from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel

from odoo.addons.pydantic import utils

from .event_stage_info import EventStageInfo
from .event_ticket_info import EventTicketInfo
from .event_type_info import EventTypeInfo


class EventShortInfo(BaseModel, metaclass=ExtendableModelMeta):
    id: int
    name: str
    date_begin: datetime
    date_end: datetime
    event_type: EventTypeInfo = pydantic.Field(None, alias="event_type_id")
    stage: EventStageInfo = pydantic.Field(None, alias="stage_id")
    note: str = None
    write_date: datetime

    class Config:
        orm_mode = True
        getter_dict = utils.GenericOdooGetter


class EventInfo(EventShortInfo):
    event_tickets: List[EventTicketInfo] = pydantic.Field([], alias="event_ticket_ids")
    seats_limited: bool
    seats_max: int = None
    seats_expected: int = None
