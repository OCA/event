/** @odoo-module */
/* Copyright 2022 Carlos Roca - Tecnativa
   Copyright 2021 Tecnativa - David Vidal
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import tour from "web_tour.tour";

export const steps = [
    {
        trigger: "a:has(span:contains('Test Event One Ticket'))",
    },
    {
        trigger: "a[href='/event']",
        extra_trigger:
            ".o_wevent_registration_single:has(span[data-oe-field='price_reduce']:contains('100.0')):has(span.js_alt_price:contains('122.00')):has(h6:contains('Test Ticket'))",
    },
    {
        trigger: "a:has(span:contains('Test Event More Tickets'))",
    },
    {
        trigger:
            "#o_wevent_tickets_collapse > div:has(span[data-oe-field='price_reduce']:contains('100.00')):has(span.js_alt_price:contains('122.00')):has(h5:contains('Test Ticket 1'))",
    },
    {
        trigger:
            "#o_wevent_tickets_collapse > div:has(span[data-oe-field='price_reduce']:contains('100.00')):not(:has(span.js_alt_price)):has(h5:contains('Test Ticket 2'))",
    },
];

tour.register(
    "website_event_sale_b2x_alt_price_b2b",
    {
        test: true,
        url: "/event",
    },
    steps
);
