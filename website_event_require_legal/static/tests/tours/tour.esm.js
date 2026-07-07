/* Copyright 2025 Tecnativa - Pilar Vargas
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_event_require_legal", {
    url: "/event",
    test: true,
    steps: () => [
        {
            content: "Click on the Design Fair event",
            trigger: 'article:contains("Test event for require legal")',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Click on Register modal tickets button",
            trigger: 'button:contains("Register")',
            run: "click",
        },
        {
            trigger: "button.a-submit",
            run: "click",
        },
        // Cannot proceed until the terms are accepted.
        {
            trigger:
                "button[type='submit'].btn.btn-primary:not(.o_wait_lazy_js):contains('Confirm Registration')",
            run: "click",
        },
        {
            content: "Accept legal terms",
            trigger: "#accepted_event_legal_terms",
            run: "click",
        },
        {
            trigger:
                ".modal#modal_attendees_registration:not(.o_inactive_modal) button[type=submit].btn-primary",
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Check container of confirmed registrations",
            trigger: ".o_wereg_confirmed",
        },
    ],
});
