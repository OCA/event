/* Copyright 2026 TechnoLibre - Mathieu Benoit
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {registry} from "@web/core/registry";

// Tour 1: Public (anonymous) user on an event with require_login enabled.
// Expected: the login-required modal appears instead of the registration form.
registry.category("web_tour.tours").add("website_event_require_login_public", {
    url: "/event",
    test: true,
    steps: () => [
        {
            content: "Go to the event requiring login",
            trigger:
                'a[href*="/event/test-event-require-login-tour-"][href$="/register"]',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Open ticket registration modal",
            trigger: 'button:contains("Register")',
            run: "click",
        },
        {
            content: "Click Register (ticket defaults to 1)",
            trigger: "button.a-submit:enabled",
            run: "click",
        },
        {
            content: "Login-required modal body is visible",
            trigger:
                "#modal_attendees_registration.o_wevent_require_login_modal .modal-body",
        },
        {
            content: "Login link points to /web/login",
            trigger:
                '#modal_attendees_registration.o_wevent_require_login_modal a.btn-primary[href*="/web/login"]',
        },
        {
            content: "Close the login-required modal",
            trigger:
                "#modal_attendees_registration.o_wevent_require_login_modal .js_goto_event",
            run: "click",
        },
    ],
});

// Tour 2: Authenticated (portal) user on the same event.
// Expected: the normal attendee registration form appears, NOT the login modal.
registry.category("web_tour.tours").add("website_event_require_login_auth", {
    url: "/event",
    test: true,
    steps: () => [
        {
            content: "Go to the event requiring login",
            trigger:
                'a[href*="/event/test-event-require-login-tour-"][href$="/register"]',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Open ticket registration modal",
            trigger: 'button:contains("Register")',
            run: "click",
        },
        {
            content: "Click Register (ticket defaults to 1)",
            trigger: "button.a-submit:enabled",
            run: "click",
        },
        {
            content: "Attendee registration form appears (normal flow, no login modal)",
            trigger: "form#attendee_registration",
        },
        {
            content: "Close the attendee registration modal",
            trigger: "#modal_attendees_registration .btn-close",
            run: "click",
        },
    ],
});
