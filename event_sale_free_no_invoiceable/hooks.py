# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    """Make non invoiceable existing event lines with price 0."""
    lines = env["sale.order.line"].search(
        [
            ("event_ticket_id", "!=", False),
            ("price_unit", "=", 0),
            ("invoice_status", "=", "to invoice"),
        ]
    )
    lines.qty_to_invoice = 0
