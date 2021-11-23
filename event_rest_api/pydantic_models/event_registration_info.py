# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

import pydantic

from odoo.addons.pydantic import models, utils

from .event_info import EventInfo
from .event_ticket_info import EventTicketInfo


class EventRegistrationInfo(models.BaseModel):
    id: int
    partner_id: int = None
    firstname: str = None
    lastname: str = None
    email: str = None
    event: EventInfo = pydantic.Field(..., alias="event_id")
    event_ticket: EventTicketInfo = pydantic.Field(None, alias="event_ticket_id")
    write_date: datetime

    class Config:
        orm_mode = True
        getter_dict = utils.GenericOdooGetter
