/* Copyright 2026 Carlos Lopez - Tecnativa
   Copyright 2022 Carlos Roca - Tecnativa
   Copyright 2021 Tecnativa - David Vidal
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_event_sale_b2x_alt_price_b2b", {
    url: "/event",
    steps: () => [
        {
            content: "Open the Test Event One Ticket event page",
            trigger: '.o_wevent_events_list a:contains("Test Event One Ticket")',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Open the register modal",
            trigger: 'button:contains("Register")',
            run: "click",
        },
        {
            trigger:
                ".o_wevent_registration_single:has(span[data-oe-field='price_reduce']:contains('100.00')):has(span.js_alt_price:contains('122.00'))",
        },
        {
            trigger: '.btn-primary.a-submit:contains("Register")',
            run: "click",
        },
        {
            content: "Wait the modal is shown before continue",
            trigger: ".modal.modal_shown.show form[id=attendee_registration]",
        },
        {
            trigger: ".modal#modal_attendees_registration input[name*='1-email']",
            run: "edit admin@example.com",
        },
        {
            trigger: ".modal#modal_attendees_registration input[name*='1-phone']",
            run: "edit 111 111",
        },
        {
            content: "Validate attendees details",
            trigger:
                "input[name*='1-name'], input[name*='2-name'], input[name*='3-name']",
        },
        {
            content: "Go to payment",
            trigger:
                '.modal#modal_attendees_registration button[type=submit]:contains("Go to Payment")',
            run: "click",
            expectUnloadPage: true,
        },
        {
            trigger: ".oe_cart:contains(payment method)",
        },
    ],
});
