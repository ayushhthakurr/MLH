# Python Direct X game controller server
# DirectX works with Scancodes for Direct Input
# Added UDP Networking functionality to existing Keyboard simulataions functions provided here(http://stackoverflow.com/a/23468236) thx /u/hodka!
# Quick project test for playing a game running on a laptop connected to a TV with a keyboard from another computer through the Network.
#Tested on Fallout 3, Tales of Monkey Island

# TODO: Create a UDP broadcast function for auto discovery of clients
# TODO: Try to fix some of the lag, currently holding down the keys for long periods of time creates problems.
# TODO: Simulate Mouse movements from a mouse through networking.


import socket,sys,time,ctypes
Port =1234

SendInput = ctypes.windll.user32.SendInput

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
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
    
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

#Direct X scancode definitions can be found here: http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
DIK_ESCAPE=0x01
DIK_1=0x02
DIK_2               =0x03
DIK_3               =0x04
DIK_4               =0x05
DIK_5               =0x06
DIK_6               =0x07
DIK_7               =0x08
DIK_8               =0x09
DIK_9               =0x0A
DIK_0               =0x0B
DIK_MINUS           =0x0C    #/* - on main keyboard */
DIK_EQUALS          =0x0D
DIK_BACK            =0x0E    #/* backspace */
DIK_TAB             =0x0F
DIK_Q               =0x10
DIK_W               =0x11
DIK_E               =0x12
DIK_R               =0x13
DIK_T               =0x14
DIK_Y               =0x15
DIK_U               =0x16
DIK_I               =0x17
DIK_O               =0x18
DIK_P               =0x19
DIK_LBRACKET        =0x1A
DIK_RBRACKET        =0x1B
DIK_RETURN          =0x1C    #/* Enter on main keyboard */
DIK_LCONTROL        =0x1D
DIK_A               =0x1E
DIK_S               =0x1F
DIK_D               =0x20
DIK_F               =0x21
DIK_G               =0x22
DIK_H               =0x23
DIK_J               =0x24
DIK_K               =0x25
DIK_L               =0x26
DIK_SEMICOLON       =0x27
DIK_APOSTROPHE      =0x28
DIK_GRAVE           =0x29    #/* accent grave */
DIK_LSHIFT          =0x2A
DIK_BACKSLASH       =0x2B
DIK_Z               =0x2C
DIK_X               =0x2D
DIK_C               =0x2E
DIK_V               =0x2F
DIK_B               =0x30
DIK_N               =0x31
DIK_M               =0x32
DIK_COMMA           =0x33
DIK_PERIOD          =0x34    #/* . on main keyboard */
DIK_SLASH           =0x35    #/* / on main keyboard */
DIK_RSHIFT          =0x36
DIK_MULTIPLY        =0x37    #/* * on numeric keypad */
DIK_LMENU           =0x38    #/* left Alt */
DIK_SPACE           =0x39
DIK_CAPITAL         =0x3A
DIK_F1              =0x3B
DIK_F2              =0x3C
DIK_F3              =0x3D
DIK_F4              =0x3E
DIK_F5              =0x3F
DIK_F6              =0x40
DIK_F7              =0x41
DIK_F8              =0x42
DIK_F9              =0x43
DIK_F10             =0x44
DIK_NUMLOCK         =0x45
DIK_SCROLL          =0x46    #/* Scroll Lock */
DIK_NUMPAD7         =0x47
DIK_NUMPAD8         =0x48
DIK_NUMPAD9         =0x49
DIK_SUBTRACT        =0x4A    #/* - on numeric keypad */
DIK_NUMPAD4         =0x4B
DIK_NUMPAD5         =0x4C
DIK_NUMPAD6         =0x4D
DIK_ADD             =0x4E    #/* + on numeric keypad */
DIK_NUMPAD1         =0x4F
DIK_NUMPAD2         =0x50
DIK_NUMPAD3         =0x51
DIK_NUMPAD0         =0x52
DIK_DECIMAL         =0x53    #/* . on numeric keypad */
DIK_F11             =0x57
DIK_F12             =0x58
RUN_W=0x2A
RUN_S=0x2A
RUN_A=0x2A
RUN_D=0x2A

#Mapping keyboardCommands to specific keys for use with Tales of Monkey Island...
#Probably a really bad way of doing this as it is specific for one game perhaps a
#better solution is to capture the DirectX window game and load a xml config for each one?
def convertKBCommand(input):
    print input
    
    if input=='up':
        return 0x11
    elif input=='lt':
        return 0x1E
    elif input=='rt':
        return 0x20
    elif input=='dn':
        return 0x1F
    elif input=='sp':
        return 0x39
    elif input=='rc':
        return 0x9D
    else:
        return 0x53



# Functions for pressing and releaseing the keys

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

#Starts the UDP server & will send keys into the game once a client is connected.
def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP=getAddrIP();
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((IP,1234))
    
    print 'started on',IP,'with Port #', Port
    print 'now run the Directx game and make sure the game is in the foreground';

    while True:
        result,addr=sock.recvfrom(16) 
        #print 'client sent',result
        result = result.split()
        roll = float(result[0])
        pitch = float(result[1])
        print "roll:",roll
        print "pitch:",pitch

        if(roll > 10.0):  #LEFT a
            PressKey(0x1E)
        if (roll < 10.0 and roll > -20.0):
            ReleaseKey(0x1E)

        if(roll < -20.0): #RIGHT d
            PressKey(0x20)
        if (roll < 10.0 and roll > -20.0):
            ReleaseKey(0x20)
            
        if(pitch > -30.0):    #UP w
            PressKey(0x11)
        if pitch < -30.0 and pitch > -40.0:
            ReleaseKey(0x11)
                
        if(pitch < -40.0):  #DOWN s
            PressKey(0x1F)
        if pitch < -30.0 and pitch > -40.0:
            ReleaseKey(0x1F)
            
        if(pitch < -60.0): #right_ctrl
            PressKey(0x9D)
        if pitch < -40.0 and pitch > -60.0:
            ReleaseKey(0x9D)
            
        if(pitch > 10.0):    #space
            PressKey(0x39)
        if pitch < 10.0 and pitch > -30.0:
            ReleaseKey(0x39)
            

def getAddrIP():
    return socket.gethostbyname(socket.getfqdn());


if __name__=='__main__':
    start_server()

socket.close()
