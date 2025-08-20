from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    external_link_url = fields.Char(
        string="External Registration Link",
        help="URL for external registration. If set, the registration form will "
        "redirect to this URL instead of the default Odoo registration form.",
    )
