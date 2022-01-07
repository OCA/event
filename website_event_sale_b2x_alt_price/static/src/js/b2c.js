/* Copyright 2022 Carlos Roca - Tecnativa
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("website_event_sale_b2x_alt_price.tour_b2c", function(require) {
    "use strict";

    const tour = require("web_tour.tour");
    const base = require("web_editor.base");

    var steps = [
        {
            trigger: "a:has(span:contains('Test Event One Ticket'))",
        },
        {
            trigger: "a[href='/event']",
            extra_trigger:
                ".col-lg-8:has(h6:contains('Test Ticket')):has(.event_b2x_flex_centered:has(span:has(.oe_currency_value:contains(122.00))):has(.text-muted:has(span:has(.oe_currency_value:contains(100.00)))))",
        },
        {
            trigger: "a:has(span:contains('Test Event More Tickets'))",
        },
        {
            trigger: "a.o_wevent_registration_btn:contains('Tickets')",
        },
        {
            trigger:
                ".row:has(.col-md-8:has(h5:contains('Test Ticket 1'))):has(.col-md-4:has(div:has(.event_b2x_flex_centered:has(span:has(.oe_currency_value:contains(122.00))):has(.text-muted:has(span:has(.oe_currency_value:contains(100.00)))))))",
        },
        {
            trigger:
                ".row:has(.col-md-8:has(h5:contains('Test Ticket 2'))):has(.col-md-4:has(div:has(.event_b2x_flex_centered:has(span:has(.oe_currency_value:contains(100.00))):not(:has(.text-muted:has(.js_alt_price))))))",
        },
    ];

    tour.register(
        "website_event_sale_b2x_alt_price_b2c",
        {
            url: "/event",
            test: true,
            wait_for: base.ready(),
        },
        steps
    );

    return {
        steps: steps,
    };
});
