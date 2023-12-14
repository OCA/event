import re

from odoo import api, models

from odoo.addons.http_routing.models.ir_http import slug


class Event(models.Model):
    _inherit = "event.event"

    # ------------------------------------------------------
    # Action button
    # ------------------------------------------------------

    def action_dup_event_and_web(self):
        new_event = self.duplicate_event_and_website({"new_name": self.name})
        return {
            "view_type": "form",
            "view_mode": "form",
            "res_model": "event.event",
            "type": "ir.actions.act_window",
            "res_id": new_event.id,
        }

    def duplicate_event_and_website(self, default_dict: dict = None):
        """
        Create a new event along with its website pages

        One view as an inheritance there other one might not if only the title has been
        changed
        If the structure of the view hasn't been changed, the view with inherit_id won't
        be created therefore the copy won't happen even if the title only has been
        changed.

        :param default_dict: A dict of default value that will be used as new event
        properties use the key "new_name" to give a specific name to the new event
        :return: The new event
        """
        self.ensure_one()
        new_event = None
        if self.website_menu:
            # If the name is not provided for the copy then the new event take the
            # same name as the original event
            new_event = self.copy(default=default_dict)  # Copy current event
            key_part = f"{slug(self)}"

            views_to_copy = self.env["ir.ui.view"].search(
                [("key", "like", key_part), ("inherit_id", "!=", False)]
            )

            for view in views_to_copy:
                # Order of creation matter for the later delete
                new_inherited_view = view.inherit_id.copy()
                new_view = view.copy()

                # Replace ids in keys for each view
                new_view.update(
                    {
                        "key": self.replace_key_id(new_view.key, new_event.id),
                        "inherit_id": new_inherited_view.id,
                    }
                )
                new_inherited_view.update(
                    {"key": self.replace_key_id(new_inherited_view.key, new_event.id)}
                )
        else:
            new_event = self.copy()

        return new_event

    def replace_key_id(self, key: str, replace_id: int) -> str:
        """
        This method is used to replace the id that has been added
        in the key. During the copy process the view will keep the
        old reference id, therefore it needs to be changed to the new
        one

        :param key (str): the key you want to change the id in
        :param replace_id (int): the id you wish the change for
        :return (str): the new key
        """
        # regex = r"(?<=-)[0-9]+"
        # new_key = re.sub(regex, str(replace_id), key, count=0, flags=re.MULTILINE)
        # return new_key

        regex = r"(?<=-)([0-9]+-*)+"
        result = re.sub(regex, str(replace_id), key, count=0, flags=re.MULTILINE)

        return result

    # ------------------------------------------------------
    # Default functions
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CRUD methods (ORM overrides)
    # ------------------------------------------------------

    @api.returns("self", lambda value: value.id)
    def copy_data(self, default: dict = None) -> [dict]:
        """
        Inheritance of copy_data() from models module in order to counter the spread of
        the string 'copy' in the new event name.

        :param default: The default dict containing fields and their value for the copy
        :return: A list of dictionnary (default) that key will be used as fields during
        the copy process
        """
        self.ensure_one()
        if default.get("new_name"):
            default["name"] = default["new_name"]
            default.pop("new_name")
        return super().copy_data(default)

    @api.ondelete(at_uninstall=True)
    def _flush_website_event_menus_and_views(self):
        """
        Make sure both associated views and menus of an event are deleted when the last
        is deleted.
        """
        for event in self:
            if event.website_menu:
                website_menu_events = self.env["website.event.menu"].search(
                    [("event_id", "=", event.id)]
                )

                menus = []
                key = None
                for website_menu_event in website_menu_events:
                    menus.append(website_menu_event.menu_id)
                    if key is None and website_menu_event.view_id.key:
                        view = website_menu_event.view_id
                        # The key we are looking for is not the same as the menu one,
                        # we separate the menu name from the key to be able to identify
                        # all views regardless of the menu. The later views will be
                        # deleted
                        key = view.get_website_event_view_key()

                menu_parents = {menu.parent_id for menu in menus}
                for parent in menu_parents:
                    parent.unlink()

                if key:
                    views = self.env["ir.ui.view"].search(
                        [("key", "like", key)], order="id"
                    )
                    view_list = [view for view in views]
                    view_list.reverse()

                    for view in view_list:
                        view.unlink()

    def _create_menu(self, sequence, name, url, xml_id, menu_type):
        """
        Ensure the menu is created with the right view. Before this override the menus
        were referencing a wrong view. For 2 website events with the same name for
        instance "golf-tournament", two views were created, golf-tournament and
        golf-tournament-1

        The second view whould never be called because the menu of the second
        website_event would refer to the view of the first website_event and
        not of the second

        This behaviour has been identified of use of key which has no unicity constraint
        """
        website_menu = super()._create_menu(sequence, name, url, xml_id, menu_type)

        website_event_menu = (
            self.env["website.event.menu"]
            .sudo()
            .search([("menu_id", "=", website_menu.id)])
        )
        view_id = website_event_menu.view_id
        if view_id:
            view_id.update({"key": f"{view_id.key}-{self.id}"})
            key = view_id.get_website_event_menu_key()
            url_splitted = website_menu.url.split("/")
            url_splitted[-1] = key

            website_menu.update({"url": "/".join(url_splitted)})
        return website_menu
