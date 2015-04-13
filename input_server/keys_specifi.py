import win32api
import win32con
import win32gui
import win32ui
import win32service
import os
import time

def f_click(pycwnd):
    x=300
    y=300
    lParam = y <<15 | x
    pycwnd.SendMessage(win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam);
    pycwnd.SendMessage(win32con.WM_LBUTTONUP, 0, lParam);

def get_whndl():
    whndl = win32gui.FindWindowEx(0, 0, None, 'Untitled - Notepad')
    return whndl

def make_pycwnd(hwnd):       
    PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
    return PyCWnd

def send_input_hax(pycwnd, msg):
    f_click(pycwnd)
    for c in msg:
        if c == "\n":
            pycwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            pycwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            pycwnd.SendMessage(win32con.WM_CHAR, ord(c), 0)
    pycwnd.UpdateWindow()

whndl = get_whndl()

def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        hwnds[win32gui.GetClassName(hwnd)] = hwnd
    return True

hwnds = {}
win32gui.EnumChildWindows(whndl, callback, hwnds)
whndl = hwnds['Edit']

pycwnd = make_pycwnd(whndl)
msg = "It works !\n"
send_input_hax(pycwnd,msg)