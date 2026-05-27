* Tree only: an event can't be shared between two siblings without going through
  their common parent. For arbitrary M2M sharing, use ``event_multi_company``.
* The opt-in flag does not apply to events with no company (always visible).
* Backend visibility broadens too: parent company users see opted-in descendants'
  events in the backend, not just on the public website.
* ``-u event`` resets the rules to upstream; re-update this module to re-apply.
