# TPLink Archer C2300 device tracker for Home Assistant

The `tplink_c2300` platform for `device_tracker` integration allows you to detect presence by looking at devices connected (via 2.4G / 5G / LAN) to a [TP-Link Archer C2300](https://www.tp-link.com/us/home-networking/wifi-router/archer-c2300/) wireless router.

This project is based on the official TP-Link integration [removed](https://github.com/home-assistant/core/pull/27936) from Home Assistant, somewhat active [fork](https://github.com/ericpignet/home-assistant-tplink_router/) for other TP-Link devices, and the [C2300 API client](https://github.com/Electry/TPLink-C2300-APIClient/).

## Installation
Copy `tplink_c2300` folder into your `custom_components`

TP-Link devices typically only allow one login at a time to the admin console.  This integration will count towards your one allowed login. Depending on how aggressively you configure device_tracker you may not be able to access the admin console of your TP-Link device without first stopping Home Assistant.
Home Assistant takes a few seconds to login, collect data, and log out. If you log into the admin console manually, remember to log out so that Home Assistant can log in again.

I recommend setting the time interval to 60s.

## Configuration

To enable this device tracker, add the following lines to your `configuration.yaml`:

```yaml
# Example configuration.yaml entry
device_tracker:
  - platform: tplink_c2300
    host: YOUR_ROUTER_IP
    password: !secret tplink_c2300_password
    interval_seconds: 60
    consider_home: 120
```

Configuration variables:

- **host** (*Required*): The IP address of your router, e.g., 192.168.1.1.
- **password** (*Required*): The plain-text password for your given local admin account.
- **interval_seconds** (*Optional*): Seconds between each scan for new devices. (aka. how often should HASS connect to the router) (Default: 12)
- **consider_home** (*Optional*): Seconds to wait till marking someone as not home after not being seen.

You don't need to fill in any **username** field, as the username is hardcoded to `admin` on the latest C2300 firmware.

See the [device tracker integration page](https://www.home-assistant.io/integrations/device_tracker/) for instructions how to configure the people to be tracked.

## Supported devices

- Archer C2300 v2.0 with firmware 1.1.1 Build 20200918 rel.67850(4555)

Other devices/firmwares may or may not work, depending on how the authentication is handled in the router firmware.
If your device is not on the list, you can still give it a try and let me know if it works or not, I'll update the documentation.

I will not be adding support to any other (not working) device, but you may open up a request [here](https://github.com/ericpignet/home-assistant-tplink_router/issues).
