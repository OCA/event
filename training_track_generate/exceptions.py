# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from openerp import _, exceptions


class EventTrackGeneratorError(exceptions.ValidationError):
    def __init__(self):
        self.name = _("Error(s) with the event track generator.")
        self.args = (self.name, self.value)


class NoWeekdaysError(EventTrackGeneratorError):
    value = "You must select at least one weekday."
