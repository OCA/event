/* Copyright 2026 INVITU (<https://www.invitu.com>)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

(function () {
    "use strict";

    document.addEventListener("change", function (ev) {
        var input = ev.target.closest(".o_wevent_attachment_input");
        if (!input || !input.files.length) return;

        var maxSizeMb = parseInt(input.dataset.maxSize || "0", 10);
        if (!maxSizeMb) return;

        var file = input.files[0];
        var maxBytes = maxSizeMb * 1024 * 1024;

        var feedback =
            input.nextElementSibling &&
            input.nextElementSibling.classList.contains("o_wevent_attachment_error")
                ? input.nextElementSibling
                : null;

        if (file.size > maxBytes) {
            input.value = "";
            if (!feedback) {
                feedback = document.createElement("small");
                feedback.className = "text-danger o_wevent_attachment_error";
                input.after(feedback);
            }
            feedback.textContent =
                "File exceeds the maximum allowed size of " + maxSizeMb + " MB.";
        } else if (feedback) {
            feedback.remove();
        }
    });
})();
