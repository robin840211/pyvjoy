"""vJoy constants and enumerations"""

# DLL filename
DLL_FILENAME = "vJoyInterface.dll"

# HID Usage IDs for axes
HID_USAGE_X = 0x30
HID_USAGE_Y = 0x31
HID_USAGE_Z = 0x32
HID_USAGE_RX = 0x33
HID_USAGE_RY = 0x34
HID_USAGE_RZ = 0x35
HID_USAGE_SL0 = 0x36
HID_USAGE_SL1 = 0x37
HID_USAGE_WHL = 0x38
HID_USAGE_POV = 0x39

# Validity checking ranges
HID_USAGE_LOW = HID_USAGE_X
HID_USAGE_HIGH = HID_USAGE_POV

# vJoy Device Status
VJD_STAT_OWN = 0   # Owned by this application
VJD_STAT_FREE = 1  # Not owned by any application
VJD_STAT_BUSY = 2  # Owned by another application
VJD_STAT_MISS = 3  # Missing or driver down
VJD_STAT_UNKN = 4  # Unknown

### CUSTOM ADDS ###

# Axis value ranges
AXIS_MIN = 0x0000
AXIS_MAX = 0x8000
AXIS_MID = 0x4000

# POV ranges
POV_NEUTRAL = -1
DISC_POV_MIN = 0
DISC_POV_MAX = 3
CONT_POV_MIN = 0
CONT_POV_MAX = 35999

# Device limits
MIN_DEVICE_ID = 1
MAX_DEVICE_ID = 16
MAX_BUTTONS = 128
MAX_POVS = 4

# Human-readable status names
VJD_STAT_NAMES = {
    VJD_STAT_OWN: "Owned by this application",
    VJD_STAT_FREE: "Free",
    VJD_STAT_BUSY: "Owned by another application",
    VJD_STAT_MISS: "Missing",
    VJD_STAT_UNKN: "Unknown"
}
