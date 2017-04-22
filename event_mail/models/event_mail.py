# -*- coding: utf-8 -*-
# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventMailSchedulerTemplate(models.Model):
    _name = 'event.mail.scheduler.template'
    _inherit = 'event.mail'

    event_id = fields.Many2one(required=False)
    event_mail_template_id = fields.Many2one(
        comodel_name='event.mail.template',
        string='Event Mail Template',
        required=True,
        ondelete='cascade',
    )


class EventMailTemplate(models.Model):
    _name = 'event.mail.template'

    @api.model
    def _default_scheduler_template_ids(self):
        return self.env['event.event'].with_context(
            by_pass_config_template=True)._default_event_mail_ids()

    name = fields.Char()
    scheduler_template_ids = fields.One2many(
        comodel_name='event.mail.scheduler.template',
        inverse_name='event_mail_template_id',
        string='Mail Schedule',
        default=_default_scheduler_template_ids,
    )
