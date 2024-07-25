odoo.define("website_event_sale_seat_reserve", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    tour.register(
        "tour_website_event_sale_seat_reserve",
        {
            test: true,
            url: "/event",
        },
        [
            {
                content: "Go to the `Events` page",
                trigger: 'a[href*="/event"]:contains("Business workshops"):first',
            },
            {
                content: "Select 1 unit of `Standard` ticket type",
                extra_trigger:
                    '#wrap:not(:has(a[href*="/event"]:contains("Business workshops")))',
                trigger: "select:eq(0)",
                run: "text 1",
            },
            {
                content: "Click on `Order Now` button",
                extra_trigger: "select:eq(1):has(option:contains(2):propSelected)",
                trigger: '.btn-primary:contains("Register")',
            },
            {
                content: "Fill attendees details",
                trigger: 'form[id="attendee_registration"] .btn:contains("Continue")',
                run: function () {
                    $("input[name='1-name']").val("Att1");
                    $("input[name='1-phone']").val("111 111");
                    $("input[name='1-email']").val("att1@example.com");
                },
            },
            {
                content: "Validate attendees details",
                extra_trigger: "input[name='1-name']",
                trigger: 'button:contains("Continue")',
            },
        ]
    );
});
