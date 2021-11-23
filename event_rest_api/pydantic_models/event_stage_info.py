# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo.addons.pydantic import models, utils


class EventStageInfo(models.BaseModel):
    id: int
    name: str
    sequence: int = None
    pipe_end: bool = None
    write_date: datetime

    class Config:
        orm_mode = True
        getter_dict = utils.GenericOdooGetter
