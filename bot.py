from typing import Optional

import ctypes
import time
import pygetwindow as gw

SendInput = ctypes.windll.user32.SendInput

Q = 0x10
D = 0x20

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
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def SetSkyrimForeground():
    win = gw.getWindowsWithTitle("Skyrim Special Edition")[0]
    win.activate()
    time.sleep(3) # Let Skyrim some time to get running properly

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hWnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    if buf.value:
        return buf.value
    else:
        return None

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def SendKey(hexKeyCode):
    PressKey(hexKeyCode)
    time.sleep(0.1)
    ReleaseKey(hexKeyCode)

# Setting amount of sleep needs special attention
def SetSleep():
    time.sleep(2)
    PressKey(D)
    timeToSetDays = time.time() + 1
    while time.time() < timeToSetDays:
        PressKey(D)
        time.sleep(0.001)
        ReleaseKey(D)

completedDays = 0
moneyGrinded = 0
def GrindMoney():
    SendKey(Q)
    SetSleep()
    SendKey(Q)
    time.sleep(30)

    global completedDays
    completedDays += 1
    global moneyGrinded
    moneyGrinded += 250

    print("Completed day %s - %s money grinded" % (completedDays, moneyGrinded))

if __name__ == '__main__':
    SetSkyrimForeground()
    while (getForegroundWindowTitle() == "Skyrim Special Edition"):
        GrindMoney()
    else:
        print("Skyrim not in foreground - script stopping")
        exit(0)
