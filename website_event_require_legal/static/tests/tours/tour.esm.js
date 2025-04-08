/** @odoo-module **/

/* Copyright 2025 Tecnativa - Pilar Vargas
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_event_require_legal", {
    url: "/event",
    test: true,
    steps: () => [
        {
            trigger:
                'a[href^="/event/test-event-for-require-legal-"][href$="/register"]',
            run: "click",
        },
        {
            trigger:
                '.container.d-none button[data-bs-target="#modal_ticket_registration"]',
            run: "click",
        },
        {
            trigger: "button.a-submit",
            run: "click",
        },
        // Cannot proceed until the terms are accepted.
        {
            trigger: "button[type='submit'].btn.btn-primary:not(.o_wait_lazy_js)",
            run: "click",
        },
        {
            content: "Accept legal terms",
            trigger: "#accepted_event_legal_terms",
            run: "click",
        },
        {
            trigger: "button[type='submit'].btn.btn-primary:not(.o_wait_lazy_js)",
            run: "click",
        },
        {
            content: "Check container of confirmed registrations",
            trigger: ".o_wereg_confirmed_attendees",
        },
    ],
});
