# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventTypeMail(models.Model):
    _inherit = "event.type.mail"

    group_by_email = fields.Boolean(
        string="Group by email",
        help="If enabled, in the case of multiple registrations having "
        "the same email address, a single grouped email will be sent.\n\n"
        "NOTE: If the email template has a report, it will be rendered for "
        "all registrations and attached in separate files.\n"
        "The registrations recordset is available in the context and can be used "
        "to render the email body. ie: object.env.context.get('records').",
        default=True,
    )

    @api.model
    def _get_event_mail_fields_whitelist(self):
        # Override. Add group_by_email field to whitelist so that
        # it's copied from Event Type when it changes.
        res = super()._get_event_mail_fields_whitelist()
        res.append("group_by_email")
        return res
