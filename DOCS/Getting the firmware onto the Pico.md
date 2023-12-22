# Getting the firmware onto the Pico.

## Preparing the Pico
You should ensure the pico's flash memory has been completely cleared of other code by 

- Boot Pico in Developement Mode. To do so hold the `bootsel` button while
plugging the pico in.

- Drag the `flashnuke.uf2` firmware file onto the `RPI-RP2` drive to ensure the
Pico's memory has been completely cleared.[Flash Nuke
Download](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#resetting-flash-memory).

> **&#9432;** When developing for the pico, be sure to commment out the Watchdog
Timer in the `Sensor` class, as it will cause the Pico to reboot and disconnect
anytime an error is encountered, without emiting error information to your
developement environment, leading to a very frustrating experience. This can
happen in sneaky ways as well, such as if you previously had added a file that
was run on boot by the pico that contained code that ran the WDT, hence the
admonition to use the `flashnuke` firmware any time you are changing software on
the pico.

- When the `RPI-RP2` drive re-appears, drag the [latest MicroPython
firmware](https://micropython.org/download/RPI_PICO_W/) onto it. Be sure to get
the firmware for the Pico-W rather than Pico, as the `network` module is needed.

## Uploading Files


### Files to upload

- `main.py`: This is the file that is loaded by the Pico on boot. It should
contain a call to whatever run command your program requires. For examples look
in the `examples/mains` directory. If you would like to use one of these, simply
copy it to the Pico and rename to `main.py` so that MicroPython loads it on
boot.

- `sensor.py`: This file contains the base class definition to initialize the
Pico for use with the `Sensor-Hub` ecosystem.

- **I2C driver files**: Files that provide definitions to take measurements from
I2C sensors, must provide a measurement method that can be handed to the
`Sensor` class instance as a no-arguement function.

- `util.py`: Provides functionality such as automated network connectivity.

## After upload

Once the files are uploaded to the Pico, it should be ready to run. Upon first
boot and connection, the Pico should automatically download and install the
required `mqtt` micropython library. This may cause an error that seems to cause
the Pico to hang when it is finished installing, but should function normally
upon power cycling. Then as long as `Sensor-Hub` is within Wi-Fi range, it
should now connect and begin loggin data automatically.


## Other Tools

- [rshell](https://github.com/dhylands/rshell)

-
[MicroPico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)(VSCode
Extension)
