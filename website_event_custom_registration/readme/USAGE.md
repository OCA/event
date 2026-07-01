On the public event page, the registration block adapts to the selected
mode:

- **Native ticketing**: the standard *Register* button and ticket modal.
- **Free / No registration**: the configured message, with no ticket
  controls and no "Sold Out" / "Closed" labels.
- **External registration**: a *Get Tickets* button linking to the external
  portal, opening in a new tab.

Once registrations close (the event has ended, is sold out or was
cancelled), free and external events show Odoo's standard "Registrations
Closed" notice like native ones, unless **Keep Custom Text When Closed** is
enabled on the event — then the custom message or button stays visible.

The routing applies everywhere the core registration block is rendered: the
event page's main call to action, the (desktop and mobile) sidebar, and the
event sub-menu, so the experience stays consistent across the site.
