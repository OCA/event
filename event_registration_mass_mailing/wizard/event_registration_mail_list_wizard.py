# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EventRegistrationMailListWizard(models.TransientModel):
    _name = "event.registration.mail.list.wizard"
    _description = "Create contact mailing list"

    mail_list = fields.Many2one(
        comodel_name="mail.mass_mailing.list", string="Mailing list"
    )
    event_registrations = fields.Many2many(
        comodel_name="event.registration",
        relation="mail_list_wizard_event" "_registration",
    )

    def add_to_mail_list(self):
        contact_obj = self.env["mail.mass_mailing.contact"]
        for registration in self.env.context.get("active_ids", []):
            registration = self.env["event.registration"].browse(registration)
            if contact_obj.search(
                [
                    ("email", "=", registration.email),
                    ("list_ids", "in", self.mail_list.id),
                ]
            ):
                continue
            contact_obj.create(
                {
                    "email": registration.email,
                    "name": registration.name,
                    "list_ids": [[6, 0, [self.mail_list.id]]],
                }
            )
