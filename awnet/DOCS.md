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
