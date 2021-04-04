# Copyright 2016 OpenSynergy Indonesia
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    contact_ids = fields.Many2many(
        string="Contacts",
        comodel_name="res.partner",
        help="Partners available to attend attendees requests by default for "
        "events of this type.",
    )
