# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.addons.base.res.res_request import referencable_models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def _origin_id_selection(self):
        """Models that could be linked to the registration."""
        # Configured referencable models
        result = referencable_models(
            self, self.env.cr, self.env.user.id, self.env.context)

        # Sale order line is required for the quotation generator system
        if "sale.order.line" not in (model[0] for model in result):
            result.append(("sale.order.line", _("Sale order line")))

        return result

    invoiced_partner_id = fields.Many2one(
        "res.partner",
        "Invoiced partner",
        help="This is the partner that will recieve the invoice. It can be "
             "different from the participant's company when one company pays "
             "for registration of others' employees, or when your company "
             "organizes the event in the name of a different company. Do not "
             "fill this if it is not different from the partner.")
    origin = fields.Char(
        store=True,
        readonly=True,
        compute="_origin_compute",
        inverse="_origin_inverse")
    origin_id = fields.Reference(
        selection=_origin_id_selection,
        string="Origin",
        help="Object linked to the registration.")

    @api.multi
    @api.depends("origin_id")
    def _origin_compute(self):
        """Change :attr:`origin` according to what gets linked."""
        for s in self:
            s.origin = (s.origin_id.name_get()[0][1]
                        if s.origin_id else False)

    @api.multi
    def _origin_inverse(self):
        """Link :attr:`origin_id` to the sale order."""
        for s in self:
            s.origin_id = s.env["sale.order"].search(
                [("name", "=", s.origin)],
                limit=1) or False

    @api.model
    def _origin_inverse_all(self):
        """Perform inversion of :attr:`origin` in all records."""
        return self.search([("origin", "!=", False),
                            ("origin_id", "=", False)])._origin_inverse()

    @api.multi
    @api.returns("res.partner")
    def invoiced_partner(self):
        """Compute automatically the partner to be invoiced."""
        return self.invoiced_partner_id or self.partner_id
