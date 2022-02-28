# Copyright 2014 Tecnativa S.L. - Pedro M. Baeza
# Copyright 2015 Tecnativa S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Antonio Espinosa
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2017 Tecnativa S.L. - David Vidal
# Copyright 2018 Jupical Technologies Pvt. Ltd. - Anil Kesariya
# Copyright 2020 Tecnativa S.L. - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Link partner to events",
    "version": "14.0.1.0.1",
    "category": "Marketing",
    "author": "Tecnativa," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/event",
    "development_status": "Production/Stable",
    "license": "AGPL-3",
    "depends": ["event"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/event_event_view.xml",
        "views/event_registration_view.xml",
        "wizard/res_partner_register_event_view.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
