# -*- coding: utf-8 -*-
# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools

_INTERVALS = {
    'hours': lambda interval: relativedelta(hours=interval),
    'days': lambda interval: relativedelta(days=interval),
    'weeks': lambda interval: relativedelta(days=7 * interval),
    'months': lambda interval: relativedelta(months=interval),
    'now': lambda interval: relativedelta(hours=0),
}


class PollMailScheduler(models.Model):
    _name = 'poll.mail.scheduler'

    poll_id = fields.Many2one(
        'poll.question', string='Poll', required=True, ondelete='cascade')
    interval_nbr = fields.Integer(string='Interval', default=1)
    interval_unit = fields.Selection([
        ('now', 'Immediately'),
        ('hours', 'Hour(s)'), ('days', 'Day(s)'),
        ('weeks', 'Week(s)'), ('months', 'Month(s)')],
        string='Unit', default='hours', required=True)
    template_id = fields.Many2one(
        'mail.template', string='Email to Send',
        domain=[('model', '=', 'poll.question')], required=True,
        ondelete='restrict',
        help='This field contains the template of '
             'the mail that will be automatically sent')
    scheduled_date = fields.Datetime(
        string='Scheduled Sent Mail', compute='_compute_scheduled_date',
        store=True)
    mail_sent = fields.Boolean(string='Mail Sent on Poll')
    done = fields.Boolean(string='Sent', compute='_compute_done', store=True)

    @api.one
    @api.depends('mail_sent')
    def _compute_done(self):
        self.done = self.mail_sent

    @api.one
    @api.depends('interval_unit', 'interval_nbr', 'poll_id.end_date')
    def _compute_scheduled_date(self):
        if not self.poll_id.end_date:
            self.scheduled_date = False
        else:
            date, sign = self.poll_id.end_date, -1
            self.scheduled_date = datetime.strptime(
                date, tools.DEFAULT_SERVER_DATETIME_FORMAT) + \
                _INTERVALS[self.interval_unit](sign * self.interval_nbr)

    @api.one
    def execute(self):
        if not self.mail_sent:
            self.poll_id.mail_participants(self.template_id.id)
            self.write({'mail_sent': True})
        return True

    @api.model
    def run(self, autocommit=False):
        schedulers = self.search([
            ('done', '=', False),
            ('scheduled_date', '<=', datetime.strftime(
                fields.datetime.now(), tools.DEFAULT_SERVER_DATETIME_FORMAT))])
        for scheduler in schedulers:
            scheduler.execute()
            if autocommit:
                self.env.cr.commit()
        return True
