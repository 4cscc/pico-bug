# Four Corners Sensor Firmware

![Pico Basic Architecture](./DOCS/BasicArchitecture.jpg)

This is the software used by the 4CSCC `Sensor-Hub` ecosystem to record data from various sensors, and then transmit that data via MQTT packet to a `Sensor-Hub` server/broker.

- Designed to be used on Raspberry Pi Pico rp2040 based boards, but could be
used on any board that has a Micropython port.

- See [documentation](./DOCS/) for how to define and register various external sensors.
