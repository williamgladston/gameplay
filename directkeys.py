import ctypes
import time

# This code only works on Windows
SendInput = ctypes.windll.user32.SendInput

# Define Virtual Key Codes
VK_LEFT = 0x4B   # 'K' key
VK_RIGHT = 0x4D  # 'M' key
# You can also use: 0x41 = 'A', 0x44 = 'D', 0x25 = Left Arrow, 0x27 = Right Arrow

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(
        wVk=hexKeyCode,
        wScan=0,
        dwFlags=0x0008,  # KEYEVENTF_SCANCODE
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(
        wVk=hexKeyCode,
        wScan=0,
        dwFlags=0x0008 | 0x0002,  # KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    while True:
        print("Pressing 'K'...")
        PressKey(VK_LEFT)
        time.sleep(1)
        print("Releasing 'K'...")
        ReleaseKey(VK_LEFT)
        time.sleep(1)

        print("Pressing 'M'...")
        PressKey(VK_RIGHT)
        time.sleep(1)
        print("Releasing 'M'...")
        ReleaseKey(VK_RIGHT)
        time.sleep(1)