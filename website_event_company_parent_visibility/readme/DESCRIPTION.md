Lets events of subsidiary companies be displayed on parent companies' websites
(and to parent companies' backend users), with an opt-in flag per subsidiary.

Visibility follows ``res.company.parent_id``. Same pattern as Odoo's own
``product`` module, with the opposite direction (``child_of`` instead of
``parent_of``).
