from owrx.config import Config
from owrx.locator import Locator
from owrx.property import PropertyFilter
from owrx.property.filter import ByPropertyName
import logging

logger = logging.getLogger(__name__)


 
class ReceiverDetails(PropertyFilter):
    def __init__(self):
        super().__init__(
            Config.get(),
            ByPropertyName(
                "receiver_name",
                "receiver_location",
                "receiver_asl",
                "receiver_gps",
                "photo_title",
                "photo_desc",
                "black_mod",
                "status_button",
                "log_button",
                "receiver_button",
                "map_button",
                "settings_button",
                "rx_usage_policy_page",
                "pseudo_session_timeout", 
                "ts_start",
                "default_time_tick",
                "default_ret_step",                                                                             
            )
        )

    def __dict__(self):
        receiver_info = super().__dict__()
        try:
            receiver_info["locator"] = Locator.fromCoordinates(receiver_info["receiver_gps"])
        except ValueError as e:
            logger.error("invalid receiver location, check in settings: %s", str(e))
        return receiver_info
