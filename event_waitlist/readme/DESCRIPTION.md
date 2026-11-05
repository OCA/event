Waiting list for sold-out events (courses, classes, workshops).

When an event or a ticket is fully booked, people can join a waiting list.
As soon as a seat becomes free (a registration is cancelled, archived or
deleted, or the capacity is increased), the waiting list moves up
automatically, in one of two modes chosen per event:

- **Offer the seat** (default): the first person receives an email with a
  link and has a deadline (12 hours by default) to accept. The seat is
  reserved for them meanwhile and cannot be booked by anyone else. If the
  deadline passes or the person declines, the next person gets the offer.
- **Register automatically**: the first person is registered right away
  and receives the normal registration confirmation.

Other features:

- One waiting list per event; an entry may target a specific ticket.
- People asking for several seats keep their position; a freed seat goes
  to the first person whose request fits.
- No offers after the event has started; the deadline never goes beyond
  the start of the event.
- Editable email templates: entry confirmed (with the position), seat
  offered, seat confirmed, offer expired. Every email contains a link to
  leave the list.
- Token links for attendees (no record ids in URLs). Links in emails only
  open a page; actions require a click on that page, so email scanners
  cannot accept or decline seats by following links.
- Duplicate entries (same email, same event) are refused.
- Seat assignment is serialized per event, so two cancellations at the same
  time can never give away more seats than are free or offer one seat twice.
- Entries are deleted automatically a configurable number of days after the
  event (data protection).
- Every step is logged in the chatter of the event.

The website part (sign-up form, button instead of "Sold Out") is in
`website_event_waitlist`.
