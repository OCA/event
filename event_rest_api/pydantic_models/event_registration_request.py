# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from typing import List

from odoo.addons.pydantic import models


class EventRegistrationRequest(models.BaseModel):

    firstname: str
    lastname: str
    email: str
    phone: str = None
    event_ticket_id: int = None


class EventRegistrationRequestList(models.BaseModel):

    event_registration_requests: List[EventRegistrationRequest] = []
