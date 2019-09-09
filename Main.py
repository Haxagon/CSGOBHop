import win32gui
import win32process
import win32api
import pymem
import sys
import os

local_offset = 0xCF5A4C
flag_offset = 0x104
force_jump_offset = 0x51AB48C

#Main Process
window = win32gui.FindWindow(0, ('Counter-Strike: Global Offensive'))
if(window):
    pid = win32process.GetWindowThreadProcessId(window)
    process = pymem.Pymem()
    process.open_process_from_id(pid[1])
    entry = process.process_base
else:
    print('Open CSGO.')
    sys.exit()

#Modules
modules = process.list_modules
while(modules != None):
    var = next(modules)
    if(var[0].name == 'client_panorama.dll'):
        c_dll = var[1]
        break

#LocalPlayer
local_player = process.read_bytes(c_dll + local_offset,4)
local_player = int.from_bytes(local_player,byteorder='little')
flag = process.read_int(local_player + flag_offset)

#KeyState, Def Key = Num5
key = win32api.GetKeyState(0x65)
while(win32api.GetKeyState(0x65) == key):
    while(win32api.GetKeyState(0x20) == -128 or win32api.GetKeyState(0x20) == -127):
          flag = process.read_int(local_player + flag_offset)
          if(flag == 256):
              process.write_int(c_dll + force_jump_offset, 4)
          else:
              process.write_int(c_dll + force_jump_offset, 5)

    
