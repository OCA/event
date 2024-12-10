/** @odoo-module */

/* Copyright 2022 Carlos Roca - Tecnativa
   Copyright 2021 Tecnativa - David Vidal
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {registry} from "@web/core/registry";
import wsTourUtils from "@website_sale/js/tours/tour_utils";

registry.category("web_tour.tours").add("website_event_sale_b2x_alt_price_b2b", {
    test: true,
    url: "/event",
    steps: () => [
        {
            content: "Open the Test Event One Ticket event page",
            trigger: '.o_wevent_events_list a:contains("Test Event One Ticket")',
        },
        {
            content: "Open the register modal",
            trigger: 'button:contains("Register")',
        },
        {
            extra_trigger:
                ".o_wevent_registration_single:has(span[data-oe-field='price_reduce']:contains('100.00')):has(span.js_alt_price:contains('122.00'))",
            trigger: '.btn-primary.o_wait_lazy_js:contains("Register")',
        },
        {
            content: "Validate attendees details",
            extra_trigger:
                "input[name*='1-name'], input[name*='2-name'], input[name*='3-name']",
            trigger: 'button[type=submit]:contains("Go to Payment")',
        },
        wsTourUtils.goToCart({quantity: 1}),
    ],
});
