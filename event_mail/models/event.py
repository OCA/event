# Copyright 2017 Tecnativa - Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.model
    def _default_event_mail_template_id(self):
        company = self.env['res.company']._company_default_get('event.event')
        return company.event_mail_template_id

    event_mail_template_id = fields.Many2one(
        comodel_name='event.mail.template',
        string='Mail Template Scheduler',
        default=_default_event_mail_template_id,
    )

    @api.onchange('event_mail_template_id')
    def _onchange_event_mail_template_id(self):
        vals = [(6, 0, [])]
        if self.event_mail_template_id.exists():
            for scheduler in \
                    self.event_mail_template_id.scheduler_template_ids:
                vals.append((0, 0, {
                    'interval_nbr': scheduler.interval_nbr,
                    'interval_unit': scheduler.interval_unit,
                    'interval_type': scheduler.interval_type,
                    'template_id': scheduler.template_id.id,
                }))
            self.event_mail_ids = vals

    @api.onchange('event_type_id')
    def _onchange_type(self):
        """If a template is already set, we'll override the event.type
           schedulers"""
        if not self.event_mail_template_id:
            return super()._onchange_type()
