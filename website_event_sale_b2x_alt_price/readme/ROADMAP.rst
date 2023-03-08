* When the public pricelist is set to display discounts in customer's face and
  the website is set to display prices tax included, the discounted price will
  appear always as tax excluded and produce weird scenarios. This is Odoo's
  bug and not this module's. It has been notified as OPW-2518694 but it doesn't
  look like it's going to be fixed any soon. In v16, event price discounts from
  pricelist don't even work and for v17 there's an ongoing refactoring work.
