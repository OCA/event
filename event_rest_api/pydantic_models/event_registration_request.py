# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from typing import List

from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel


class EventRegistrationRequest(BaseModel, metaclass=ExtendableModelMeta):

    firstname: str
    lastname: str
    email: str
    phone: str = None
    mobile: str = None
    event_ticket_id: int = None


class EventRegistrationRequestList(BaseModel, metaclass=ExtendableModelMeta):

    event_registration_requests: List[EventRegistrationRequest] = []
