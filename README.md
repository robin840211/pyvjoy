### *This is a fork version of [pyvjoy from maxofbritton](https://github.com/maxofbritton/pyvjoy) which based off [tidzo's package](https://github.com/tidzo/pyvjoy), with just few changes and less API different.*


# pyvjoy

pyvjoy is a set of Python bindings for [vJoy](https://sourceforge.net/projects/vjoystick/).

With this library you can easily set Axis and Button values on any vJoy device.  
Low-level bindings are provided in pyvjoy._sdk as well as a (hopefully) slightly more 'Pythonic' API in the pyvjoy.VJoyDevice() object.


## Requirements

Install vJoy from https://sourceforge.net/projects/vjoystick/.

It is recommended to also install the vJoy Monitor and Configure vJoy programs. These should be an option during installation.


## Installation

Simply install from pip:

`pip install pyvjoy`

After vJoy and pyvjoy have been installed, you may need to copy the vJoyInterface.dll file from your installation location to the location of the python package.


## Usage
```python
import pyvjoy

# Pythonic API, item-at-a-time
j = pyvjoy.VJoyDevice(1)

# turn button number 15 on
# Note: the args are (buttonID, state) whereas vJoy's native API is the other way around.
j.set_button(15, 1)

# turn button 15 off again
j.set_button(15, 0)

# Set X axis to fully left
j.set_axis(pyvjoy.HID_USAGE_X, 0x1)

# Set X axis to fully right
j.set_axis(pyvjoy.HID_USAGE_X, 0x8000)

# Also implemented:

j.reset()
j.reset_buttons()
j.reset_povs()
```

### The 'efficient' method as described in vJoy's docs - set multiple values at once

`j.data`

`>>> <pyvjoy._sdk._JOYSTICK_POSITION_V2 at 0x....>`

```python
j.data.lButtons = 19 # buttons number 1,2 and 5 (1+2+16)
j.data.wAxisX = 0x2000 
j.data.wAxisY= 0x7500

# send data to vJoy device
j.update()
```


## Note

Currently vJoyInterface.dll is looked for inside the pyvjoy directory, only ensure works with x86, not guaranteed with x64.

Only the desired version 2.1.8.38 of the file to be use while install from pip, but should not bother even using 2.1.9.1's vJoy.

[Pointy's Joystick Test App](https://www.planetpointy.co.uk/joystick-test-application/) or even vJoy Feeder by vJoy are both useful when testing vJoy and this library.

Lower-level API just wraps the functions in the DLL as thinly as possible, with some attempt to raise exceptions instead of return codes.
