# Home Assistant Add-on: AWNET

Local data transfer between Ambient Weather weather station and Home Assistant.

## About

You can use this add-on to take advantage of the new "Custom Server" feature in AWNET available in Firmware [4.2.8](https://ambientweather.com/support) on the WS-2902A, WS-2902B, WS-2902C, WS-2000 And WS-5000. I have tested this using my WS-2902C. It presents a webserver that will accept the polling from the WS device. It then calls a service provided by the [Ambient Weather Station - Local](https://github.com/tlskinneriv/awnet_local) custom integration to ingest data.

This add-on and integration combo are a work in progress. Any feedback and/or contributions are appreciated. Credit to [dancwilliams](https://github.com/dancwilliams) for the [initial add-on](https://github.com/dancwilliams/hassio-addons/tree/master/awnet) that this was forked from.

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg

## Usage Without Home Assistant OS

See the [documentation](https://github.com/tlskinneriv/hassio-addons/blob/master/awnet/DOCS.md#non-ha-os-options) about usage of the container and script within in the event you are running HA in Docker or HA Core.
