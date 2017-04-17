# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from .base import BaseCase


class AppendingTemplateCase(BaseCase):
    """Test method :meth:`~._onchange_contents_layout`."""

    create_method = "new"

    def tearDown(self):
        self.course = self.course.with_context(lang="en_US")

        for cols in range(2, 5):
            previous = self.course.contents or ""
            single = '<div class="col-xs-%d">Column %%d</div>' % (
                12 / cols)

            self.course.contents_layout = cols
            self.course._onchange_contents_layout()
            self.assertEqual(
                self.course.contents,
                previous + "".join(map(lambda n: single % n,
                                       range(1, cols + 1))))
            self.assertFalse(self.course.contents_layout)
            self.course.contents = previous

    def test_when_empty(self):
        """User asks for template before writing any contents."""
        self.course.contents = False

    def test_when_full(self):
        """User asks for template after writing some contents"""
        self.course.contents = u"Jojooó"
