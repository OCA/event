odoo.define("website_event_sale_check_order_before_payment.payment", function(require) {
    "use strict";

    const publicWidget = require("web.public.widget");

    publicWidget.registry.WebsiteSalePayment.include({
        /**
         * @override
         */
        start: function() {
            const res = this._super.apply(this, arguments);
            // This.$payButton is used in core logic to enable/disable the pay button according whether the customer
            // ticked the cgv checkbox.
            // If we want to keep the same behavior, we need to update the attribute with the new id of the button
            this.$payButton = $("button#o_payment_form_check_order_and_pay");
            this.$checkbox.trigger("change");
            return res;
        },
    });
});
