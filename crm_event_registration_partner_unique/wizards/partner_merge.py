# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, models
from openerp.exceptions import UserError


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _update_foreign_keys(self, cr, uid,
                             src_partners, dst_partner, context=None):
        self.get_fk_on(cr, 'res_partner')
        for table, column in cr.fetchall():
            partners = (map(int, src_partners))
            partners.append(dst_partner.id)
            if table == 'event_registration':
                query = """ SELECT r.event_id, e.name, count(r.partner_id)
                            FROM event_registration r
                            LEFT JOIN event_event e on r.event_id = e.id
                            WHERE e.forbid_duplicates
                            AND r.partner_id IN %s
                            GROUP BY r.event_id, e.name
                            """
                cr.execute(query, (tuple(partners),))
                for event_id, name, count_partner in cr.fetchall():
                    if count_partner > 1:
                        raise UserError(
                            _("These action would produce duplicated partners "
                              "in an event wich has it forbidden.\n"
                              "Event ID: %d\n"
                              "Name: %s") % (event_id, name))
        return super(
            BasePartnerMergeAutomaticWizard, self)._update_foreign_keys(
            cr, uid, src_partners, dst_partner, context)
