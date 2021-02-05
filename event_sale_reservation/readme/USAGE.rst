To know how many reservations exist for a given event type:

#. Go to *Events > Configuration > Event Categories* and pick or create one.
#. There's a new smart button called *Reserved seats* with that count.
#. Click on it to get to the sales orders where the seats got reserved.

But that counter will be probably zero when you install, so let's see how to
increase it.

To create an event reservation product:

#. Go to *Sales > Products > Products*.
#. Create one.
#. Set its basic info (name, price...) and go to *Sales* tab.
#. Under *Events*, tick *Is an event reservation*.
#. Select one *Event type for reservations*.
#. Save.

From now on, you can sell event reservations for that event type. To do it:

#. Go to *Sales > Orders > Quotations*.
#. Create one.
#. Set its basic info (customer, date...) and go to *Order lines* tab.
#. Click *Add a product*.
#. Select the event reservation product you created above.
#. Set its info (quantity, price...).
#. Save that line and the quotation.

At this point, the reservation is not yet confirmed, so if you go to the event
type, the smart button will still count zero.

To confirm those reservations:

#. Go to the quotation you just created (if you are not there yet).
#. Click on *Confirm*.

Now, if you go to the event type form, the smart button will indicate how many
reserved seats exist.

If you want to convert those reservations into real event registrations:

#. Go to the quotation you just created (if you are not there yet).
#. Click on *Register in event*.
#. In the wizard you see, set the *Event* and *Event Ticket* for all the order
   lines you want to convert into registrations.
#. If there is any line you still don't want to convert, remove it from the
   wizard.
#. Click on *Next*.
#. A new wizard will appear, where you will be able to specify the name, email
   and phone of each one of the attendees. If you don't do it, they will get
   that info from the sales order customer.
#. After that's done, click on *Apply*.

At this point, the sales order lines will be modified to include the ticket
product instead of the reservation product, and the event reservations have
been created, linked to those lines.

If the ticket was free, the registrations are confirmed. Otherwise, they are
kept as draft until an invoice is created for the sales order, and paid. But
that is just upstream ``event_sale`` module in action.
