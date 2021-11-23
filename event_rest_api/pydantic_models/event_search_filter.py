# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from typing import List

from odoo.addons.pydantic import models


class EventSearchFilter(models.BaseModel):

    id: int = None
    name: str = None
    start_after: datetime = None
    end_before: datetime = None
    event_type_ids: List[int] = None
    stage_ids: List[int] = None
