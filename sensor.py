import logging
import requests
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the OpenAI Vision sensor platform."""
    if discovery_info is None:
        return

    name = discovery_info["name"]
    ha_url = discovery_info["ha_url"]
    hass_token = discovery_info["hass_token"]
    add_entities([OpenAIVisionSensor(hass, name, ha_url, hass_token)], True)

class OpenAIVisionSensor(Entity):
    """Representation of an OpenAI Vision sensor."""

    def __init__(self, hass, name, ha_url, hass_token):
        """Initialize the sensor."""
        self.hass = hass
        self._name = name
        self._ha_url = ha_url
        self._hass_token = hass_token
        self._state = "waiting"
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"openai_vision_{self._name.lower()}_response"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor."""
        if not self.entity_id:
            _LOGGER.warning(f"Entity ID for {self._name} is not set. Skipping update.")
            return

        url = f"{self._ha_url}/api/states/{self.entity_id}"
        headers = {
            "Authorization": f"Bearer {self._hass_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self._state = data['state']
            self._attributes = data['attributes']
        else:
            _LOGGER.error(f"Error fetching data from {url}: {response.status_code} - {response.text}")
