# Copyright 2021 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class Event(models.Model):
    _name = "event.event"
    _inherit = ["event.event", "mail.activity.mixin"]


class EventRegistration(models.Model):
    _name = "event.registration"
    _inherit = ["event.registration", "mail.activity.mixin"]
