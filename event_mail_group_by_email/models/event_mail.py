# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventMail(models.Model):
    _inherit = "event.mail"

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

    def execute(self):
        # Override. Split super() calls in two, adding the context key
        # group_by_email when needed
        grouped = self.filtered("group_by_email")
        return (
            super(EventMail, self - grouped).execute()
            and super(EventMail, grouped.with_context(group_by_email=True)).execute()
        )
