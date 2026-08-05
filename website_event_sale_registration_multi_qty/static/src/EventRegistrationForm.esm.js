/** @odoo-module **/
import EventRegistrationForm from "website_event.website_event";

EventRegistrationForm.include({
    on_click: function () {
        var result = this._super.apply(this, arguments);
        return result.then(this.proxy("addMultiQtyEvents"));
    },
    addMultiQtyEvents: function () {
        jQuery("#attendee_registration .use-multi-qty input").change(
            this.proxy("onChangeUseMultiQty")
        );
    },
    onChangeUseMultiQty: function (ev) {
        // Select the form in a roundabout way because when the popup is closed,
        // it's not cleaned up so there are multiple form elements with the same id
        var $form = jQuery(".js_website_submit_form:visible").filter(function (
                ids,
                element
            ) {
                return element.id === "attendee_registration";
            }),
            $target = jQuery(ev.target),
            ticket_id = $target.data("ticket-id"),
            show_others = $target.filter(":checked").length === 0;
        var $attendee_containers = $form
            .find("input[name$=-event_ticket_id]")
            .filter(function (idx, element) {
                return element.value === ticket_id;
            })
            .parents(".modal-body[data-hide-multi-qty]");
        $attendee_containers.toggle(show_others);
        $attendee_containers.find("input").attr("disabled", !show_others);
    },
});
