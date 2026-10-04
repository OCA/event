# Copyright 2026 Riccardo Fiore
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Shared helpers for the private-event access gate.

Kept here (rather than on the controller) so both the controller and the
``ir.http`` routing override can ask the same question — "may this visitor
see this private event?" — without one importing the other.
"""

# Session list of event ids the current visitor has unlocked this session.
SESSION_KEY = "event_private_unlocked"


def is_event_manager(env):
    """Event managers always bypass the gate (preview / edit the page)."""
    return env.user.has_group("event.group_event_user")


def event_visitor_unlocked(env, session, event):
    """Whether the current visitor may see this (possibly private) event.

    :param env: the (real, non-sudo) environment, used for the manager check.
    :param session: the HTTP session holding the unlocked-event id list.
    :param event: the ``event.event`` record (may be sudo'd; only ``id`` and
        ``is_private`` are read).
    """
    if not event.is_private:
        return True
    if is_event_manager(env):
        return True
    return event.id in (session.get(SESSION_KEY) or [])
