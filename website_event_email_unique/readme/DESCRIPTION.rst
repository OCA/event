This module will check whether an attendee already registered with the same e-mail address.
If this is the case, then depending on configuration, the new registration will either:
#. Replace the previous one
#. Be ignored

This module is quite similar in implemented function to event_registration_partner_unique,
except that you do not have to get a partner for each attendee, you only make check on e-mail.
Also there is no dependency to partner_event module since it is not needed here.
