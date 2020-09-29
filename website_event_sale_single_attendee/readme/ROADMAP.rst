* This module breaks the feature of website_event_questions, and a glue module
  must restrict the checkbox 'Ask each attendee' (`event.question.is_individual`)
  to False, if the event is set with 'Single Attendee Registration'.
* As only one e-mail is registered, the attendee will receive as many e-mails as tickets he ordered.
