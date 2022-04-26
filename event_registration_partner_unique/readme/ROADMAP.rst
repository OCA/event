* This module is intended for backend use, so the validation error is enough
  to show the user what is wrong,
* When *website_event* is installed, and public users try to register more
  than one attendee, this will trigger a validation error as the attendee
  partner is duplicated. The error shown is 500 internal server error.
* It would be necessary to have a new module which depends on *website_event*
  plus this one to prevent said issue.
* Another problem would arise when used with *event_sale* module, because it
  would try to use "Sale Order" contact as attendee and that will lead to the
  issue of duplicated attendees if trying to buy access to the same event
  more than once.
