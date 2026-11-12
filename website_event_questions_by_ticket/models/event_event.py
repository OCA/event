# Copyright 2019 Tecnativa - Pedro M. Baeza
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    def _get_specific_questions(self, ticket_id):
        self.ensure_one()
        return self.specific_question_ids.filtered(
            lambda x: (
                not x.restricted_ticket_ids or ticket_id in x.restricted_ticket_ids.ids
            )
        )

    def _get_general_questions(self, ticket_ids):
        self.ensure_one()
        return self.general_question_ids.filtered(
            lambda x: (
                not x.restricted_ticket_ids
                or (set(ticket_ids) & set(x.restricted_ticket_ids.ids))
            )
        )


class EventQuestion(models.Model):
    _inherit = "event.question"

    restricted_ticket_ids = fields.Many2many(
        comodel_name="event.event.ticket",
        string="Limited to tickets",
        domain="[('event_id', '=', parent.id)]",
        ondelete="restrict",
    )
