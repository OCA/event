# -*- coding: utf-8 -*-
# Copyright 2017,2018 IT-Projects LLC - Ivan Yelizariev
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Restricted access to confirm unpaid tickets",
    "summary": "Only event manager can confirm unpaid tickets",
    "version": "10.0.1.0.0",
    "category": "Event Management",
    "website": "https://github.com/OCA/event",
    "author": "IT-Projects LLC, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event_sale",
    ],
    "data": [
        "views/event_registration_view.xml",
    ],
    "demo": [
        "views/tour_views.xml",
    ],
}
