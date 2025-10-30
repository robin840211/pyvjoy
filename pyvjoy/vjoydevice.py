"""Object-oriented interface for vJoy devices"""

import time
from pyvjoy.constants import *
from pyvjoy.exceptions import *
import pyvjoy._sdk as _sdk


class VJoyDevice:
    """
    Object-oriented API for a vJoy Device
    
    Usage:
        # Method 1: Manual management
        device = VJoyDevice(rID=1)
        device.set_button(1, True)
        device.reset()
        
        # Method 2: Context manager (recommended)
        with VJoyDevice(rID=1) as device:
            device.set_button(1, True)
    """
    
    def __init__(self, rID=None, data=None):
        """
        Initialize vJoy device
        
        Args:
            rID: Report ID (1-16)
            data: Optional pre-initialized data structure
            
        Raises:
            vJoyException: If vJoy is not enabled or device cannot be acquired
        """
        if rID is None:
            raise ValueError("rID (Report ID) must be specified")
        
        if not (1 <= rID <= 16):
            raise ValueError("rID must be between 1 and 16")
        
        self.rID = rID
        self._sdk = _sdk
        self._vj = self._sdk._vj
        self._acquired = False
        
        # Initialize data structure
        if data:
            self.data = data
        else:
            self.data = self._sdk.CreateDataStructure(self.rID)
        
        # Check vJoy is enabled
        _sdk.vJoyEnabled()
        
        # Acquire device
        _sdk.AcquireVJD(rID)
        self._acquired = True
    
    def set_button(self, buttonID, state):
        """
        Set a given button to On or Off
        
        Args:
            buttonID: Button number (1-128)
            state: True/1 for pressed, False/0 for released
            
        Returns:
            True if successful
        """
        if not (1 <= buttonID <= 128):
            raise ValueError("buttonID must be between 1 and 128")
        
        return self._sdk.SetBtn(bool(state), self.rID, buttonID)
    
    def set_axis(self, AxisID, AxisValue):
        """
        Set a given Axis to a value
        
        Args:
            AxisID: Axis ID (HID_USAGE_X, HID_USAGE_Y, etc.)
            AxisValue: Axis value (0x0000 - 0x8000, where 0x4000 is center)
            
        Returns:
            True if successful
        """
        # Validate axis value range
        if not (0x0000 <= AxisValue <= 0x8000):
            raise ValueError(
                "AxisValue must be between 0x0000 and 0x8000, got 0x{:04X}".format(AxisValue))
        
        return self._sdk.SetAxis(AxisValue, self.rID, AxisID)
    
    def set_disc_pov(self, PovID, PovValue):
        """
        Set discrete POV hat position
        
        Args:
            PovID: POV ID (1-4)
            PovValue: Direction (-1=neutral, 0=N, 1=E, 2=S, 3=W)
            
        Returns:
            Result from SDK
        """
        return self._sdk.SetDiscPov(PovValue, self.rID, PovID)
    
    def set_cont_pov(self, PovID, PovValue):
        """
        Set continuous POV hat position
        
        Args:
            PovID: POV ID (1-4)
            PovValue: Angle in 1/100 degrees (-1=neutral, 0-35999)
            
        Returns:
            Result from SDK
        """
        return self._sdk.SetContPov(PovValue, self.rID, PovID)
    
    def reset(self):
        """Reset all axes and buttons to default values"""
        return self._sdk.ResetVJD(self.rID)
    
    def reset_data(self):
        """Reset the data structure to default (does not affect device)"""
        self.data = self._sdk.CreateDataStructure(self.rID)
    
    def reset_buttons(self):
        """Reset all buttons on the vJoy Device to default"""
        return self._sdk.ResetButtons(self.rID)
    
    def reset_povs(self):
        """Reset all POV hats on the vJoy Device to default"""
        return self._sdk.ResetPovs(self.rID)
    
    def update(self):
        """
        Send the stored Joystick data to the device in one go
        This is the efficient method for updating multiple controls
        """
        return self._sdk.UpdateVJD(self.rID, self.data)
    
    def reacquire(self):
        """
        Relinquish and re-acquire the device (useful for recovery from errors)
        
        Returns:
            True if successful
        """
        try:
            # First, try to relinquish if we think we own it
            if self._acquired:
                try:
                    self._sdk.RelinquishVJD(self.rID)
                except:
                    pass  # Ignore errors during relinquish
            
            # Wait a moment for the device to be released
            time.sleep(0.1)
            
            # Try to acquire again
            self._sdk.AcquireVJD(self.rID)
            self._acquired = True
            
            # Reset to default state
            self.reset()
            
            return True
        except Exception as e:
            self._acquired = False
            raise vJoyFailedToAcquireException(f"Failed to reacquire device: {e}")
    
    def relinquish(self):
        """Manually relinquish control of the device"""
        if self._acquired:
            self._sdk.RelinquishVJD(self.rID)
            self._acquired = False
    
    # Context manager support
    def __enter__(self):
        """Enter context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and relinquish device"""
        self.relinquish()
        return False
    
    def __del__(self):
        """Destructor - attempt to relinquish device"""
        # Note: __del__ is not guaranteed to be called
        # Use context manager or manual relinquish() for reliable cleanup
        try:
            self.relinquish()
        except:
            pass  # Ignore errors during cleanup

