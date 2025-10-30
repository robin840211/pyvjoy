"""
vJoy SDK wrapper for Python
Provides low-level interface to vJoyInterface.dll
"""

import os
import sys
from ctypes import *
from ctypes import wintypes    # Makes this lib work in Python36

from pyvjoy.constants import *
from pyvjoy.exceptions import *

# Determine architecture and DLL path
if sys.maxsize > 2**32:
    arch_folder = 'utils' + os.sep + 'x64'
else:
    arch_folder = 'utils' + os.sep + 'x86'

dll_path = os.path.dirname(__file__) + os.sep + arch_folder + os.sep + DLL_FILENAME

# Load vJoy DLL
try:
    _vj = cdll.LoadLibrary(dll_path)
except OSError as e:
    sys.exit("Unable to load vJoy SDK DLL. Ensure that {} is present\n{}".format(
        DLL_FILENAME, str(e)))


def vJoyEnabled():
    """
    Returns True if vJoy is installed and enabled
    
    Raises:
        vJoyNotEnabledException: If vJoy is not enabled
    """
    result = _vj.vJoyEnabled()
    if result == 0:
        raise vJoyNotEnabledException()
    return True


def DriverMatch():
    """
    Check if the version of vJoyInterface.dll and the vJoy Driver match
    
    Raises:
        vJoyDriverMismatchException: If versions don't match
    """
    result = _vj.DriverMatch()
    if result == 0:
        raise vJoyDriverMismatchException()
    return True


def GetVJDStatus(rID):
    """
    Get the status of a given vJoy Device
    
    Args:
        rID: Report ID (1-16)
        
    Returns:
        Status code (VJD_STAT_OWN, VJD_STAT_FREE, etc.)
    """
    return _vj.GetVJDStatus(rID)


def AcquireVJD(rID):
    """
    Attempt to acquire a vJoy Device
    
    Args:
        rID: Report ID (1-16)
        
    Returns:
        True if successful
        
    Raises:
        vJoyFailedToAcquireException: If acquisition fails
    """
    result = _vj.AcquireVJD(rID)
    if result == 0:
        # Check status for more specific error
        status = GetVJDStatus(rID)
        if status == VJD_STAT_OWN:
            raise vJoyFailedToAcquireException(
                "Cannot acquire vJoy Device because it is already owned by this application")
        elif status == VJD_STAT_BUSY:
            raise vJoyFailedToAcquireException(
                "Cannot acquire vJoy Device because it is owned by another application")
        elif status == VJD_STAT_MISS:
            raise vJoyFailedToAcquireException(
                "Cannot acquire vJoy Device because it is missing or driver is down")
        else:
            raise vJoyFailedToAcquireException(
                "Cannot acquire vJoy Device (Status: {})".format(status))
    return True


def RelinquishVJD(rID):
    """
    Relinquish control of a vJoy Device
    
    Args:
        rID: Report ID (1-16)
        
    Returns:
        True if successful
        
    Raises:
        vJoyFailedToRelinquishException: If relinquish fails
    """
    result = _vj.RelinquishVJD(rID)
    if result == 0:
        raise vJoyFailedToRelinquishException()
    return True


def SetBtn(state, rID, buttonID):
    """
    Sets the state of a vJoy Button to on or off
    
    Args:
        state: Button state (True/1 for pressed, False/0 for released)
        rID: Report ID (1-16)
        buttonID: Button number (1-128)
        
    Returns:
        True if successful
        
    Raises:
        vJoyButtonException: If button operation fails
    """
    result = _vj.SetBtn(state, rID, buttonID)
    if result == 0:
        raise vJoyButtonException("Failed to set button {} on device {}".format(
            buttonID, rID))
    return True


def SetAxis(AxisValue, rID, AxisID):
    """
    Sets the value of a vJoy Axis
    
    Args:
        AxisValue: Axis value (typically 0x0000 - 0x8000)
        rID: Report ID (1-16)
        AxisID: Axis ID (HID_USAGE_X, HID_USAGE_Y, etc.)
        
    Returns:
        True if successful
        
    Raises:
        vJoyInvalidAxisException: If axis operation fails
    """
    # Validate AxisID
    if AxisID < HID_USAGE_LOW or AxisID > HID_USAGE_HIGH:
        raise vJoyInvalidAxisException(
            "Invalid Axis ID: {}. Must be between {} and {}".format(
                AxisID, HID_USAGE_LOW, HID_USAGE_HIGH))
    
    result = _vj.SetAxis(AxisValue, rID, AxisID)
    if result == 0:
        raise vJoyInvalidAxisException(
            "Failed to set axis {} on device {}".format(AxisID, rID))
    return True


def SetDiscPov(PovValue, rID, PovID):
    """
    Write Value to a given discrete POV defined in the specified VDJ
    
    Args:
        PovValue: POV value (-1 for neutral, 0-3 for directions)
        rID: Report ID (1-16)
        PovID: POV ID (1-4)
        
    Returns:
        Result from DLL
        
    Raises:
        vJoyInvalidPovValueException: If POV value is invalid
        vJoyInvalidPovIDException: If POV ID is invalid
    """
    if PovValue < -1 or PovValue > 3:
        raise vJoyInvalidPovValueException(
            "Discrete POV value must be -1 to 3, got {}".format(PovValue))
    
    if PovID < 1 or PovID > 4:
        raise vJoyInvalidPovIDException(
            "POV ID must be 1 to 4, got {}".format(PovID))
    
    return _vj.SetDiscPov(PovValue, rID, PovID)


def SetContPov(PovValue, rID, PovID):
    """
    Write Value to a given continuous POV defined in the specified VDJ
    
    Args:
        PovValue: POV value (-1 for neutral, 0-35999 for angle in 1/100 degrees)
        rID: Report ID (1-16)
        PovID: POV ID (1-4)
        
    Returns:
        Result from DLL
        
    Raises:
        vJoyInvalidPovValueException: If POV value is invalid
        vJoyInvalidPovIDException: If POV ID is invalid
    """
    if PovValue < -1 or PovValue > 35999:
        raise vJoyInvalidPovValueException(
            "Continuous POV value must be -1 or 0 to 35999, got {}".format(PovValue))
    
    if PovID < 1 or PovID > 4:
        raise vJoyInvalidPovIDException(
            "POV ID must be 1 to 4, got {}".format(PovID))
    
    return _vj.SetContPov(PovValue, rID, PovID)


def ResetVJD(rID):
    """
    Reset all axes and buttons to default for specified vJoy Device
    
    Args:
        rID: Report ID (1-16)
        
    Returns:
        Result from DLL
    """
    return _vj.ResetVJD(rID)


def ResetButtons(rID):
    """
    Reset all buttons to default for specified vJoy Device
    
    Args:
        rID: Report ID (1-16)
        
    Returns:
        Result from DLL
    """
    return _vj.ResetButtons(rID)


def ResetPovs(rID):
    """
    Reset all POV hats to default for specified vJoy Device
    
    Args:
        rID: Report ID (1-16)
        
    Returns:
        Result from DLL
    """
    return _vj.ResetPovs(rID)


def UpdateVJD(rID, data):
    """
    Pass data for all buttons and axes to vJoy Device efficiently
    
    Args:
        rID: Report ID (1-16)
        data: JOYSTICK_POSITION_V2 structure
        
    Returns:
        Result from DLL
    """
    return _vj.UpdateVJD(rID, pointer(data))


def CreateDataStructure(rID):
    """
    Create and initialize a JOYSTICK_POSITION_V2 structure
    
    Args:
        rID: Report ID (1-16)
        
    Returns:
        Initialized JOYSTICK_POSITION_V2 structure
    """
    data = _JOYSTICK_POSITION_V2()
    data.set_defaults(rID)
    return data


class _JOYSTICK_POSITION_V2(Structure):
    """
    vJoy device position data structure (Version 2)
    Matches JOYSTICK_POSITION_V2 from vJoyInterface.h
    """
    _fields_ = [
        ('bDevice', c_byte),
        ('wThrottle', c_long),
        ('wRudder', c_long),
        ('wAileron', c_long),
        ('wAxisX', c_long),
        ('wAxisY', c_long),
        ('wAxisZ', c_long),
        ('wAxisXRot', c_long),
        ('wAxisYRot', c_long),
        ('wAxisZRot', c_long),
        ('wSlider', c_long),
        ('wDial', c_long),
        ('wWheel', c_long),
        ('wAxisVX', c_long),
        ('wAxisVY', c_long),
        ('wAxisVZ', c_long),
        ('wAxisVBRX', c_long),
        ('wAxisVRBY', c_long),
        ('wAxisVRBZ', c_long),
        ('lButtons', c_long),           # 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed (bit 0 = button 1, bit 31 = button 32)
        
        ('bHats', wintypes.DWORD),      # Lower 4 bits: POV HAT 1 switch or 16-bit of continuous HAT switch
        ('bHatsEx1', wintypes.DWORD),   # Lower 4 bits: POV HAT 2 switch or 16-bit of continuous HAT switch
        ('bHatsEx2', wintypes.DWORD),   # Lower 4 bits: POV HAT 3 switch or 16-bit of continuous HAT switch
        ('bHatsEx3', wintypes.DWORD),   # Lower 4 bits: POV HAT 4 switch or 16-bit of continuous HAT switch
        
        # JOYSTICK_POSITION_V2 Extension
        ('lButtonsEx1', c_long),        # Buttons 33-64
        ('lButtonsEx2', c_long),        # Buttons 65-96
        ('lButtonsEx3', c_long),        # Buttons 97-128
    ]
    
    def set_defaults(self, rID):
        """
        Initialize structure with default values
        
        Args:
            rID: Report ID (1-16)
        """
        self.bDevice = c_byte(rID)
        self.bHats = 0xFFFFFFFF      # -1 (neutral position)
        self.bHatsEx1 = 0xFFFFFFFF
        self.bHatsEx2 = 0xFFFFFFFF
        self.bHatsEx3 = 0xFFFFFFFF
