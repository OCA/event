# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventEventRibbon(models.Model):
    _name = "event.event.ribbon"
    _description = "Event Event Ribbon"
    _order = "sequence ASC, id"

    name = fields.Char(required=True, translate=True, size=20)
    sequence = fields.Integer(default=10)
    bg_color = fields.Char(required=True, default="#000000")
    text_color = fields.Char(required=True, default="#FFFFFF")
    position = fields.Selection(
        selection=[("left", "Left"), ("right", "Right")],
        required=True,
        default="left",
    )

    def _get_style(self):
        """
        Return the inline CSS style for this ribbon based on its
        background and text colors.
        rtype: str
        """
        return f"background-color: {self.bg_color}; color: {self.text_color};"

    def _get_css_classes(self):
        """
        Return the CSS classes for this ribbon based on style and position.
        rtype: str
        """
        css_classes = "o_ribbon o_not_editable z-index-1 "

        match self.position:
            case "left":
                css_classes += " o_ribbon_left"
            case "right":
                css_classes += " o_ribbon_right"
        return css_classes
