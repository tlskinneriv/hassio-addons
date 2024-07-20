# Documentation

## Add-On Setup

- Install this add-on to Home Assistant using the method referenced in the repository [README](https://github.com/tlskinneriv/hassio-addons/blob/master/README.md)
- Navigate to this add-on's Info tab in Home Assistant, configure it to start on boot, then start the add-on

NOTE: If the accompanying custom integration, [Ambient Weather Local](https://github.com/tlskinneriv/awnet_local), is not configured before starting this add-on,
errors will be reported in the add-on logs since it cannot contact the service for updates. See the [Configuration](https://github.com/tlskinneriv/awnet_local#configuration) section for the custom integration for setup instructions. Once the custom integration is loaded, the add-on can be restarted for service calls to work properly.

### Add-On Options

| Name                 | Default | Description                                                                                                                                                |
| -------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Log Level            | WARNING | Logging level for outputting messages to the add-on logs. INFO will show the raw data being sent to the service, DEBUG will show all available log entries |
| MAC Address Override | n/a     | Override the MAC address/PASSKEY of the messages sent by the device.                                                                                       |

## Ambient Weather Configuration

_These instructions are adapted from the Android app, but should be similar on other platforms_

- Navigate to your device in the awnet app
- Use the "Next" button in the upper right to navigate to the "Customized" page
- Configure the customized data upload with the following:
  - Protocol Type Same As: Ambient Weather
  - Server IP / Hostname: (your Home Assistant IP/hostname)
  - Path: ? (Literally the '?' character to send the data as a query string to the web server)
  - Port: (Port the add-on is listening on, default 7080)
  - Upload Interval: (user determined, how often to send data to Home Assistant)
- Click "Save" at the bottom of the form
- Use the "Finish" button in the upper right to complete configuration

## Non-HA OS Options

The following options have been minimally tested, but should work properly. By default, the container/script
will listen on all IP addresses on port 7080.

### Container Setup without HA OS (e.g. HA Docker)

Obtain the container from the GitHub registry for your platform:

- armhf: ghcr.io/tlskinneriv/armhf-addon-awnet_to_hass
- armv7: ghcr.io/tlskinneriv/armv7-addon-awnet_to_hass
- aarch64: ghcr.io/tlskinneriv/aarch64-addon-awnet_to_hass
- amd64: ghcr.io/tlskinneriv/amd64-addon-awnet_to_hass
- i386: ghcr.io/tlskinneriv/i386-addon-awnet_to_hass

Run the container with at least the following environment variables set:

- HA_API_BASE_URL: The base URL to your HA instance's API; e.g. http://homeassistant.local:8123/api/
- HA_API_AUTH_TOKEN: A long-lived access token for HA. Create one under user profile -> security.

See the header comments in the [awnet.py][awnet.py] script for additional details and settings.

### Script Setup for use with HA Core

Obtain the [awnet.py][awnet.py] script.

Run the script with at least the following environment variables set:

- HA_API_BASE_URL: The base URL to your HA instance's API; e.g. http://homeassistant.local:8123/api/
- HA_API_AUTH_TOKEN: A long-lived access token for HA. Create one under user profile -> security.

See the header comments in the [awnet.py][awnet.py] script for additional details and settings.

[awnet.py]: https://github.com/tlskinneriv/hassio-addons/blob/master/awnet/rootfs/awnet.py