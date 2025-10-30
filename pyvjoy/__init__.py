"""
pyvjoy - Python interface for vJoy virtual joystick driver

Usage:
    from pyvjoy import VJoyDevice, HID_USAGE_X
    
    with VJoyDevice(rID=1) as joystick:
        joystick.set_axis(HID_USAGE_X, 0x4000)
        joystick.set_button(1, True)
"""

__version__ = '1.0.2'
__all__ = ['VJoyDevice', 'constants', 'exceptions']

# Import constants and exceptions into package namespace
from pyvjoy.constants import *
from pyvjoy.exceptions import *

# Import main API
from pyvjoy.vjoydevice import VJoyDevice

# Note: _sdk is internal, not exposed in __all__
