This module allows to group event communications by registration email address,
and by doing so avoid flooding the customer's inbox.

When enabled, if there are multiple registrations with the same email address,
only one email will be sent.

If the email template has a report, it will be rendered for all the
attendees in the group and attached to the same email.

The attendees recordset can be accessed through the context to customize the
email template's content. It's available in the context key 'records'.
