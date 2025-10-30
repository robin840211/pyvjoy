"""vJoy related exceptions"""


class vJoyException(Exception):
    """Base exception for all vJoy errors"""
    pass


class vJoyNotEnabledException(vJoyException):
    """vJoy is not installed or not enabled"""
    pass


class vJoyFailedToAcquireException(vJoyException):
    """Failed to acquire vJoy device"""
    pass


class vJoyFailedToRelinquishException(vJoyException):
    """Failed to relinquish vJoy device"""
    pass


class vJoyButtonException(vJoyException):
    """Button operation failed"""
    pass


class vJoyDriverMismatchException(vJoyException):
    """vJoy driver and DLL version mismatch"""
    pass


class vJoyInvalidAxisException(vJoyException):
    """Invalid axis ID or operation"""
    pass


class vJoyInvalidPovValueException(vJoyException):
    """Invalid POV value"""
    pass


class vJoyInvalidPovIDException(vJoyException):
    """Invalid POV ID (must be 1-4)"""
    pass
