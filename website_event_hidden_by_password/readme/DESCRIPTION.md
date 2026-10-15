This module lets each website event be made **private**, hidden behind a
shared access password.

A private event:

- is **redacted** on the website events listing: its card shows no name,
  date, location or image, only a lock, "Private" and an optional public
  **codename** (the slug-free gate link keeps the name out of the URL too);
- is **not searchable by its real name, subtitle or venue**, and never
  leaks through the search facet counts. A visitor can only find it by
  typing its **codename**, and then it surfaces as the same redacted card,
  shown as `{codename}` (both on the events page and in the search
  autocomplete);
- shows an **info-free password wall** when opened: the event page (and its
  sub-pages) only render once the visitor enters the correct password;
- keeps its name out of every direct entry point. Guessing the integer id
  (`/event/42`), the registration page or the iCal download (`/ics`) sends
  the visitor to the gate instead of leaking the name, and the event is
  left out of `sitemap.xml`;
- keeps its password on the event record itself, next to the *Private*
  toggle, with a **Generate** button for a random one.

The password is a *shared secret* (like a webinar password), not a user
account credential: it is stored and shown in clear text and is only
readable by event managers. Managers always bypass the wall so they can
preview and edit the page.

## Scope and limitations

This module is designed to close **every entry point in Odoo core** through
which a private event could otherwise be discovered or have its details
exposed: the events listing, the search, the search autocomplete and the
filter counts, the canonical-URL redirect, direct page access, the iCal
exports and `sitemap.xml`. The access guard is applied at the routing
layer, so it also covers the standard event add-ons (tracks, agenda, booth)
without this module depending on them.

It cannot, however, protect entry points it has no knowledge of. If you
install additional modules, or otherwise make events reachable through a
custom route, report, API, feed, export or third-party integration,
securing those new entry points is **your responsibility**, typically in a
small custom bridge module (this module deliberately avoids hard
dependencies on optional add-ons).

If you discover an entry point in **Odoo core** that still exposes a
private event's name or details, please open an issue on the project's
GitHub tracker and tag the maintainer (`@odrakirmusic`) so it can be closed
in this module.
