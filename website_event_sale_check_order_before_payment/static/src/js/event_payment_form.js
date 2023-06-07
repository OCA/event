odoo.define(
    "website_event_sale_check_order_before_payment.event_payment_form",
    function(require) {
        "use strict";

        const paymentForm = require("payment.payment_form");
        const core = require("web.core");
        const _t = core._t;

        paymentForm.include({
            events: _.extend({}, paymentForm.prototype.events, {
                "click #o_payment_form_check_order_and_pay": "checkOrderAndPayEvent",
            }),

            checkOrderAndPayEvent: async function(ev) {
                ev.preventDefault();
                const order_validity_data = await this._rpc({
                    route: "/shop/check_before_payment",
                });
                if (order_validity_data.valid) {
                    return this.payEvent(ev);
                }
                this.displayError(
                    _t("The payment can't be processed"),
                    _t(order_validity_data.message || "Unexpected error")
                );
            },

            /**
             * @override
             */
            onSubmit: async function(ev) {
                const res = this._super.apply(this, arguments);
                const button = $(ev.target).find('*[type="submit"]')[0];
                if (button.id === "o_payment_form_check_order_and_pay") {
                    return await this.checkOrderAndPayEvent(ev);
                }
                return res;
            },
        });
    }
);
