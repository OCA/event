/* global DOMParser, Modal */
import EventRegistrationForm from "@website_event/js/website_event";
import {patch} from "@web/core/utils/patch";
import {rpc} from "@web/core/network/rpc";

patch(EventRegistrationForm.prototype, {
    async _onClick(ev) {
        const formEl = ev.currentTarget.closest("form");

        if (formEl.dataset.requireLogin !== "1") {
            // Standard registration flow
            return super._onClick(ev);
        }

        // Login required: support custom modal
        ev.preventDefault();
        ev.stopPropagation();
        const buttonEl = ev.currentTarget.closest("[type='submit']");
        buttonEl.disabled = true;

        const post = this._getPost();
        const modal = await rpc(formEl.action, post);
        const modalEl = new DOMParser().parseFromString(modal, "text/html").body
            .firstChild;

        const _onClose = () => {
            buttonEl.disabled = false;
            modalEl.remove();
        };
        const closeBtn = modalEl.querySelector(".btn-close");
        const gotoBtn = modalEl.querySelector(".js_goto_event");
        if (closeBtn) closeBtn.addEventListener("click", _onClose);
        if (gotoBtn) gotoBtn.addEventListener("click", _onClose);

        const formModal = Modal.getOrCreateInstance(modalEl, {
            backdrop: "static",
            keyboard: false,
        });
        formModal.show();
    },
});
