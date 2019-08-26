* This modules intended used with backend, so the validation error
  are enough to show user what is wrong, when *website_event* is installed
  public user would try register attendees.
  As soon try more than one attendee this will trigger validation error as
  the attendee partner is duplicated the error shown is 500 internal server error
  which is no appropriated.
* It would be necessary have a new module with depends on website_event and this
  one to prevent this issue.
* Another kind of problem is with *event_sale* module that would try use Sale Order
  contact as attendee that will lead to the issue of attendee duplicates if try to
  buy two times same event.
