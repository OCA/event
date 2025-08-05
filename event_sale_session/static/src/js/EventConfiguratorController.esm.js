/*
    Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr)
    Copyright 2023 Tecnativa - Carlos Roca
    @author Iván Todorovich <ivan.todorovich@gmail.com>
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {EventConfiguratorController} from "@event_sale/js/event_configurator_controller";
import {patch} from "@web/core/utils/patch";

patch(EventConfiguratorController.prototype, {
    /**
     * @override
     */
    async onRecordSaved(record) {
        const doAction = this.action.doAction;
        this.action.doAction = (actionRequest, options = {}) => {
            actionRequest.infos.eventConfiguration.event_session_id =
                record.data.event_session_id;
            return doAction(actionRequest, options);
        };
        const res = await super.onRecordSaved(...arguments);
        this.action.doAction = doAction;
        return res;
    },
});
