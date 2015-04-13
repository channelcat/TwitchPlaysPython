#!/usr/bin/python
# -*- coding: <encoding name> -*-

import sys
import json
import requests
import win32gui
import win32ui
import win32con
from time import sleep

command_list_name = sys.argv[1].strip()
command_name = sys.argv[2].strip()



command_list_string = open("commands/{}.json".format(command_list_name), "rb").read()
command_list = json.loads(command_list_string.decode('utf-8'))
commands = command_list[command_name]

keymap_string = open("keymap.json", "rb").read()
keymap = json.loads(keymap_string.decode('utf-8'))

p1_keys = keymap['players']["1"]

def _get_windows_bytitle(title_text, exact = False):
    def _window_callback(hwnd, all_windows):
        all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    windows = []
    win32gui.EnumWindows(_window_callback, windows)
    if exact:
        return [hwnd for hwnd, title in windows if title_text == title]
    else:
        return [hwnd for hwnd, title in windows if title_text in title]

window = _get_windows_bytitle('Snes9X')[0]
win32gui.SetForegroundWindow(window)
sleep(0.01)

def remap(command):
    command['key'] = p1_keys[command['key']]
    return command

commands['commands'] = [ remap(command) for command in commands.get('commands') ]

print(commands)

requests.post('http://127.0.0.1:8100/input/queue', data=json.dumps(commands))