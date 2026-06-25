This module lets each website event choose how attendees register, beyond
Odoo's native ticketing, through a single `Registration Mode` selection:

- **Native ticketing**: Odoo's standard tickets and registration flow
  (default, unchanged behaviour).
- **Free / No registration**: no tickets; a custom rich-text message is
  shown in the registration block instead.
- **External registration**: a button redirects attendees to a foreign
  ticket portal in a new tab.

The three behaviours are combined into one Selection field to avoid the UI
state clashes and XPath conflicts that separate modules would create.

When an event is *free* or *external*, the native "Sold Out" /
"Registrations Closed" labels and the navbar register link are suppressed,
so the page never looks broken just because no native ticket is configured.

When a non-native mode is selected, the backend event form also locks the
native seat limit read-only and hides the registration statistics and
attendees smart buttons, since no native registrations are collected.
