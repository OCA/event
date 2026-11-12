# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from . import res_company

# WARNING: Order of imports matters on this module, so don't put res_company
# below the other modules since it will lead to a missing column error when
# the module is initialized for the first time since there are fields with
# default values wich refer to this new res.company field.
from . import event
from . import event_mail
from . import event_type
from . import res_config_settings
