import re

from odoo import models


class View(models.Model):
    _inherit = "ir.ui.view"

    # ------------------------------------------------------
    # Action button
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Default functions
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CRUD methods (ORM overrides)
    # ------------------------------------------------------
    SEPARATOR = "-"

    def get_website_event_menu_key(self):
        """
        Find the useful part in the view key mainely for menu creation and unlink
        during the flush.

        :return: <menu_name>-<event_name>-<event_id> key format
        """
        regex = r"(?<=\.)[a-zA-Z-]+[0-9].*"
        result = re.search(regex, self.key)
        return result[0]

    def get_website_event_view_key(self):
        """
        Find the useful part in the view key that is common to all views linked to an
        event. We can achieve that thanks to the event_ID we injected earlier in the
        view key.

        :return: <event_name>-<event_id> key format
        """
        key = self.get_website_event_menu_key()
        return self.SEPARATOR.join(key.split(self.SEPARATOR)[1:])
