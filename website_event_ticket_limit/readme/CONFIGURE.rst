On event record, add a ticket and configure **Max. per order** field.

By setting 0 on that field, the number of ticket that one can order is not limited
(and in this case you will have the 9 tickets limit as per Odoo standard).

If you set a limit higher than 9, then website will allow you to register these many
tickets (overpassing limit of 9 set by default by Odoo core module - although still
limiting to seats_limited and seats_available per event / ticket).
