# upy-segclockmulti
NTP clock with dual 7-seg displays via I2C GPIO expanders on ESP8266 in Micropython

This is intended to display multiple hour fields for different timezones, as well as a single minutes and seconds display.
I haven't gotten around to building out the hours displays yet, so I just have 4-digit minutes/seconds module displaying hours and minutes for a single timezone.

This project uses submodules. Clone with `git clone --recurse-submodules` or `git submodule init` in each submodule directory.

## BOM
- 1x esp8266 development board with USB - I used a nodemcuv2 variant
- 5x Dual 7-Segment Displays (2 built out so far)
- 4x mcp2308 8-bit I<sup>2</sup>C GPIO expander
- 3x mcp23017 16-bin I<sup>2</sup>C GPIO expander (for hours- not implemented yet)
- 2x 10K resistors for pullups
- 80x 330 ohm resistors for LED current limiting
- 1x old phone USB charger - to power it when it is on the wall

## Wiring
This section could use some expansion, but here are some high-level notes on what I'm doing.

### ESP &rarr; I<sup>2</sup>C Modules
1. VCC &rarr; VIN - the displays and GPIO expanders will be driven from the USB 5v supply
3. GND &rarr; GND
4. SDA &rarr; D1 (Pin 5) + pullup resistor to 3V3
5. SCL &rarr; D2 (Pin 4) + pullup resistor to 3V3

### Seconds/Minutes Module
Currently being used to display hours/minutes for a single timezone.

I've got 2 dual 7-segment modules mounted next to each other, with the one to the right flipped, so the dots create a colon.<br/>
Each dual display is driven by 2 mcp23008 ICs, one mounted above the display and one below, on one side of a 2.5" x 2" perfboard.<br/>
The segments are connected to the mcp ICs via 330 ohm resistors.

### Hours Module
Not built yet.

The intention is to have 3 of the dual 7-segment displays arranged vertically showing the hour in different timezones.

Each dusal 7-segment display will be driven by a mcp23017 on the I<sup>2</sup>C bus with 330 ohm resistors on each LED.

## Getting Started
- Install micropython to your board https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html
- `cp config.json.example config.json` and edit config.json to match your environment
- Upload the sources to the device - load.sh is an example using [ampy](https://github.com/adafruit/ampy) to load them over serial

## TODO
- Configurable I/O Pins
- Improve localization (Timezone and DST offsetting)
- Build out multi-hour section of display and add code to support it
