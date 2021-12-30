# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EventRegistrationMailListWizard(models.TransientModel):
    _name = "event.registration.mail.list.wizard"
    _description = "Create contact mailing list"

    mail_list = fields.Many2one(comodel_name="mailing.list", string="Mailing list")
    event_registrations = fields.Many2many(
        comodel_name="event.registration",
        relation="mail_list_wizard_event_registration",
    )

    def add_to_mail_list(self):
        registrations = self.env["event.registration"].search(
            [
                ("id", "in", self.env.context.get("active_ids", [])),
                ("email", "not in", self.mail_list.contact_ids.mapped("email")),
            ]
        )
        self.mail_list.contact_ids = [
            (0, 0, {"email": r.email, "name": r.name}) for r in registrations
        ]
