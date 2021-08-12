"""Support for TP-Link Archer C2300"""
from homeassistant.components.device_tracker import (DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (CONF_HOST, CONF_PASSWORD)
import homeassistant.helpers.config_validation as config_validation
import voluptuous as vol
import logging

from . import tplink

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): config_validation.string,
    vol.Required(CONF_PASSWORD): config_validation.string,
})

def get_scanner(hass, config):
    """Validate the configuration and return a TP-Link scanner."""
    return TPLinkDeviceScanner(config[DOMAIN])

class TPLinkDeviceScanner(DeviceScanner):
    def __init__(self, config):
        self.host = config[CONF_HOST]
        self.password = config[CONF_PASSWORD]

        self.last_results = {}

    def _add_device(self, device):
        result = {}
        result['hostname'] = device['hostname']
        result['wire_type'] = device['wire_type']
        result['ipaddr'] = device['ipaddr']
        result['macaddr'] = device['macaddr']
        self.last_results[device['macaddr']] = result

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        api = tplink.TPLinkClient(self.host)
        api.connect(self.password)
        
        clients = api.get_client_list()
        _LOGGER.debug(clients)

        if 'success' not in clients or clients['success'] == False:
            return

        self.last_results = {}

        for wireless in clients['data']['access_devices_wireless_host']:
            self._add_device(wireless)
            
        for wired in clients['data']['access_devices_wired']:
            self._add_device(wired)

        return self.last_results.keys()

    def get_device_name(self, device):
        """Get firmware doesn't save the name of the wireless device."""
        d = self.last_results.get(device)
        if d is None:
            return None

        hostname = d['hostname']

        if hostname.upper() == 'UNKNOWN' or hostname.upper() == 'WORKGROUP':
            return None

        return hostname

    def get_extra_attributes(self, device):
        return self.last_results.get(device)
