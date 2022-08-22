# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def post_init_hook(cr, registry):
    cr.execute(
        """
        UPDATE event_registration r
        SET lang = p.lang
        FROM res_partner p
        WHERE r.partner_id = p.id
    """
    )
