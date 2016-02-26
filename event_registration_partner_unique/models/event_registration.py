# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    _sql_constraints = [
        ("unique_partner_event",
         "UNIQUE(partner_id, event_id)",
         "Cannot repeat partner in the same event.")
    ]
