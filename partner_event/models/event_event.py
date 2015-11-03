# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    create_partner = fields.Boolean(string="Create Partners in registration",
                                    default=False)
