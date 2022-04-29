
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/event&target_branch=13.0)
[![Pre-commit Status](https://github.com/OCA/event/actions/workflows/pre-commit.yml/badge.svg?branch=13.0)](https://github.com/OCA/event/actions/workflows/pre-commit.yml?query=branch%3A13.0)
[![Build Status](https://github.com/OCA/event/actions/workflows/test.yml/badge.svg?branch=13.0)](https://github.com/OCA/event/actions/workflows/test.yml?query=branch%3A13.0)
[![codecov](https://codecov.io/gh/OCA/event/branch/13.0/graph/badge.svg)](https://codecov.io/gh/OCA/event)
[![Translation Status](https://translation.odoo-community.org/widgets/event-13-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/event-13-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Event management addons for Odoo

This repository includes all modules relative to event management that extends
current functionality in Odoo:

* Link with projects and plan them
* Add images to events
* Allow nested events
* ...

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[crm_event](crm_event/) | 13.0.1.1.0 | [![Yajo](https://github.com/Yajo.png?size=30px)](https://github.com/Yajo) | Link opportunities to event categories
[event_contact](event_contact/) | 13.0.1.0.0 |  | Add contacts to event and event type
[event_email_reminder](event_email_reminder/) | 13.0.1.0.0 |  | Send an email before an event start
[event_mail](event_mail/) | 13.0.1.0.0 |  | Mail settings in events
[event_registration_cancel_reason](event_registration_cancel_reason/) | 13.0.1.0.0 |  | Reasons for event registrations cancellations
[event_registration_multi_qty](event_registration_multi_qty/) | 13.0.1.0.0 |  | Allow registration grouped by quantities
[event_registration_partner_unique](event_registration_partner_unique/) | 13.0.1.0.1 |  | Enforces 1 registration per partner and event
[event_sale_registration_multi_qty](event_sale_registration_multi_qty/) | 13.0.1.0.0 |  | Allows sell registrations with more than one attendee
[event_sale_reservation](event_sale_reservation/) | 13.0.1.0.0 | [![Yajo](https://github.com/Yajo.png?size=30px)](https://github.com/Yajo) | Allow selling event registrations before the event exists
[event_sale_session](event_sale_session/) | 13.0.1.0.0 |  | Sessions sales in events
[event_session](event_session/) | 13.0.1.0.2 |  | Sessions in events
[event_session_registration_multi_qty](event_session_registration_multi_qty/) | 13.0.1.0.0 |  | Allow registration grouped by quantities in sessions
[event_track_location_overlap](event_track_location_overlap/) | 13.0.1.0.0 |  | Restrict event track location overlapping
[event_type_multi_company](event_type_multi_company/) | 13.0.1.0.0 | [![ivantodorovich](https://github.com/ivantodorovich.png?size=30px)](https://github.com/ivantodorovich) | Event Type Multi-Company
[partner_event](partner_event/) | 13.0.1.0.1 |  | Link partner to events
[sale_crm_event_reservation](sale_crm_event_reservation/) | 13.0.1.0.1 | [![Yajo](https://github.com/Yajo.png?size=30px)](https://github.com/Yajo) | Combine event reservations, opportunities and quotations
[website_event_crm](website_event_crm/) | 13.0.1.1.0 | [![Yajo](https://github.com/Yajo.png?size=30px)](https://github.com/Yajo) | Invite leads to event types on website
[website_event_filter_city](website_event_filter_city/) | 13.0.1.0.2 | [![Yajo](https://github.com/Yajo.png?size=30px)](https://github.com/Yajo) | Add a customizable top area to filter events with city
[website_event_questions_by_ticket](website_event_questions_by_ticket/) | 13.0.1.0.1 |  | Events Questions conditional to the chosen ticket
[website_event_questions_free_text](website_event_questions_free_text/) | 13.0.1.0.0 |  | Free Text Answers on Events Questions
[website_event_require_login](website_event_require_login/) | 13.0.1.0.0 |  | Website Event Require Login
[website_event_sale_b2x_alt_price](website_event_sale_b2x_alt_price/) | 13.0.1.0.1 | [![Yajo](https://github.com/Yajo.png?size=30px)](https://github.com/Yajo) | Display alt. price (B2B for B2C websites, and viceversa)
[website_event_sale_hide_ticket](website_event_sale_hide_ticket/) | 13.0.1.0.0 |  | Allow to hide event ticket from the website

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
