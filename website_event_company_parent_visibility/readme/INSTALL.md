Depends on ``website_event`` only.

The three event ir.rules (``event_event_company_rule``,
``event_registration_company_rule``, ``ir_rule_event_event_ticket_company``)
are overridden in place via ``security/event_security.xml``.

Uninstall does **not** auto-revert these rules. Run ``-u event`` afterwards
to restore the upstream domains.
