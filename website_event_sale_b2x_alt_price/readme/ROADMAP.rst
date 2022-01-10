* When the public pricelist is set to display discounts in customer's face and
  the website is set to display prices tax included, the discounted price will
  appear always as tax excluded and produce weird scenarios. This is Odoo's
  bug and not this module's. It has been notified as OPW-2518694. When it's
  fixed upstream, we should check this module still works as expected, although
  it probably should. However, it could depend on the way it's fixed.
