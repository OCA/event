# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


class BaseCase(object):
    def setUp(self, *args, **kwargs):
        result = super(BaseCase, self).setUp(*args, **kwargs)

        self.event_type_1 = self.env["event.type"].create({
            "name": u"Test êvent type 1",
        })
        self.event_type_2 = self.env["event.type"].create({
            "name": u"Test €vent type 2",
        })
        self.product = self.env["product.product"].create({
            "name": u"Test ṕroduct 1",
        })
        self.event = self.env["event.event"].create({
            "name": u"Test ëvent 1",
            "date_begin": "2015-11-26",
            "date_end": "2015-11-30",
        })

        return result
