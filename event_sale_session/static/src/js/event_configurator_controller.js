odoo.define("event_sale_session.EventConfiguratorFormController", function (require) {
    "use strict";

    const FormController = require("event.EventConfiguratorFormController");

    FormController.include({
        /**
         * @override
         */
        saveRecord: function () {
            var state = this.renderer.state.data;
            if (state.session_id) {
                return this.do_action({
                    type: "ir.actions.act_window_close",
                    infos: {
                        eventConfiguration: {
                            event_id: {id: state.event_id.data.id},
                            event_ticket_id: {id: state.event_ticket_id.data.id},
                            session_id: {id: state.session_id.data.id},
                        },
                    },
                });
            }
            return this._super.apply(this, arguments);
        },
    });

    return FormController;
});
