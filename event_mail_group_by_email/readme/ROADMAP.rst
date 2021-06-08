If Auto confirm registrations is enabled on the event, and the mail scheduler
is configured to send emails after each registration, no grouping will be applied.

This is because the scheduler would be executed one by one for each new confirmed
registration.

However, the grouping works as expected when confirming multiple registrations at once,
which is the case in normal event sale workflows.
