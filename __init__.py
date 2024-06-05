import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.helpers import discovery
import yaml

_LOGGER = logging.getLogger(__name__)

DOMAIN = "openai_vision"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required("sensors"): vol.All(cv.ensure_list, [
                    vol.Schema({vol.Required(CONF_NAME): cv.string})
                ])
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the OpenAI Vision component."""
    if DOMAIN not in config:
        return True

    # Load settings from YAML
    with open('/config/custom_components/openai_vision/settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)

    ha_url = settings['settings']['HA_URL']
    hass_token = settings['settings']['HASS_TOKEN']

    for entry in config[DOMAIN]["sensors"]:
        name = entry[CONF_NAME]
        hass.async_create_task(
            discovery.async_load_platform(hass, "sensor", DOMAIN, {"name": name, "ha_url": ha_url, "hass_token": hass_token}, config)
        )

    return True
