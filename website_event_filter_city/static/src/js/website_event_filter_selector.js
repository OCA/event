/* © 2016 Antiun Ingeniería S.L. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

"use strict";
(function ($) {
    // Apply filters when changed
    $("#website_event_filter_selector select").change(function(event){
        $(event.target).closest("form").submit();
    })
})(jQuery);
