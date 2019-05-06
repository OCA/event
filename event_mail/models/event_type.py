# Copyright 2019 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class EventType(models.Model):
    _inherit = 'event.type'

    @api.model
    def _get_default_event_type_mail_ids(self):
        if self.env.context.get('by_pass_config_template', False):
            return super()._get_default_event_type_mail_ids()
        company = self.env['res.company']._company_default_get('event.event')
        event_mail_template_id = company.event_mail_template_id
        if event_mail_template_id:
            return [{
                'template_id': line.template_id,
                'interval_nbr': line.interval_nbr,
                'interval_unit': line.interval_unit,
                'interval_type': line.interval_type}
                for line in event_mail_template_id.scheduler_template_ids]
        else:
            return []
