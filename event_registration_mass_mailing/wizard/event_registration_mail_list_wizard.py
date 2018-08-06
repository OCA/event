# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventRegistrationMailListWizard(models.TransientModel):
    _name = "event.registration.mail.list.wizard"
    _description = "Create contact mailing list"

    mail_list = fields.Many2one(
        comodel_name="mail.mass_mailing.list",
        string="Mailing list",
    )
    event_registrations = fields.Many2many(
        comodel_name="event.registration",
        relation="mail_list_wizard_event_registration",
    )

    @api.multi
    def add_to_mail_list(self):
        contact_obj = self.env['mail.mass_mailing.contact']
        registration_obj = self.env['event.registration']
        for registration_id in self.env.context.get('active_ids', []):
            registration = registration_obj.browse(registration_id)
            criteria = [('email', '=', registration.email),
                        ('list_ids', 'in', self.mail_list.ids)]
            contact_test = contact_obj.search(criteria)
            if contact_test:
                continue
            contact_vals = {
                'email': registration.email,
                'name': registration.name,
                'list_ids': [(4, self.mail_list.id)],
            }
            contact_obj.create(contact_vals)
