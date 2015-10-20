# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from .base import BaseCase


class AppendingTemplateCase(BaseCase):
    """Test method :meth:`~._onchange_append_template`."""

    create_method = "new"

    def tearDown(self):
        with self.action.with_context(lang="en_US").env.manage():
            for cols in range(2, 5):
                previous = self.action.contents
                single = '<div class="col-xs-%d">Column %%d</div>' % (
                    12 / cols)

                self.action.append_template = cols
                self.action._onchange_append_template()
                self.assertEqual(
                    self.action.contents,
                    previous + "".join(map(lambda n: single % n,
                                           range(1, cols + 1))))
                self.assertFalse(self.action.append_template)
                self.action.contents = previous

    def test_when_empty(self):
        """User asks for template before writing any contents."""
        self.action.contents = ""

    def test_when_full(self):
        """User asks for template after writing some contents"""
        self.action.contents = u"Jojooó"
