/*
    Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr)
    @author Iván Todorovich <ivan.todorovich@gmail.com>
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
odoo.define("event_sale_session.EventConfiguratorFormController", function (require) {
    "use strict";

    const FormController = require("event.EventConfiguratorFormController");

    FormController.include({
        /**
         * @override
         *
         * Send the event_session_id when the action is triggered by :meth:`~saveRecord`.
         */
        do_action: function (action) {
            const state = this.renderer.state.data;
            if (
                state.event_use_sessions &&
                action.type === "ir.actions.act_window_close" &&
                action.infos.eventConfiguration
            ) {
                action.infos.eventConfiguration.event_session_id = {
                    id: state.event_session_id.data.id,
                };
            }
            return this._super.apply(this, arguments);
        },
    });

    return FormController;
});
