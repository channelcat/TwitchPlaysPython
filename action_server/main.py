#!/usr/bin/python
# -*- coding: <encoding name> -*-

import win32gui
import win32ui
import win32con

from time import sleep, time


from PIL import Image
#import numpy

def subimg(img1,img2):
    img1=numpy.asarray(img1)
    img2=numpy.asarray(img2)

    #img1=numpy.array([[1,2,3],[4,5,6],[7,8,9]])
    #img2=numpy.array([[0,0,0,0,0],[0,1,2,3,0],[0,4,5,6,0],[0,7,8,9,0],[0,0,0,0,0]])

    img1y=img1.shape[0]
    img1x=img1.shape[1]

    img2y=img2.shape[0]
    img2x=img2.shape[1]

    stopy=img2y-img1y+1
    stopx=img2x-img1x+1

    for x1 in range(0,stopx):
        for y1 in range(0,stopy):
            x2=x1+img1x
            y2=y1+img1y

            pic=img2[y1:y2,x1:x2]
            test=pic==img1

            if test.all():
                return x1, y1

    return False

def screenshot(hwnd = None):
    from time import sleep
    if not hwnd:
        hwnd=win32gui.GetDesktopWindow()
    l,t,r,b=win32gui.GetWindowRect(hwnd)
    h=b-t
    w=r-l
    hDC = win32gui.GetWindowDC(hwnd)
    myDC=win32ui.CreateDCFromHandle(hDC)
    newDC=myDC.CreateCompatibleDC()

    myBitMap = win32ui.CreateBitmap()
    myBitMap.CreateCompatibleBitmap(myDC, w, h)

    newDC.SelectObject(myBitMap)

    newDC.BitBlt((0,0),(w, h) , myDC, (0,0), win32con.SRCCOPY)
    myBitMap.Paint(newDC)
    myBitMap.SaveBitmapFile(newDC, 'screenshot.bmp')


def _get_windows_bytitle(title_text, exact = False):
    def _window_callback(hwnd, all_windows):
        all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    windows = []
    win32gui.EnumWindows(_window_callback, windows)
    if exact:
        return [hwnd for hwnd, title in windows if title_text == title]
    else:
        return [hwnd for hwnd, title in windows if title_text in title]


def matchTemplate(baseImage, subImage):
    baseImageData = baseImage.getdata()
    subImageData = subImage.getdata()
    subMatchesNeeded = len(subImageData)

    baseWidth = baseImage.size[0]
    baseHeight = baseImage.size[1]
    subWidth = subImage.size[0]
    subHeight = subImage.size[1]
    lastUsableBaseX = baseWidth - subWidth
    lastUsableBaseY = baseHeight - subHeight

    matchOffset = 0
    matchX = 0
    matchStartX = 0
    matchStartY = 0
    matchStartOffset = 0
    baseY = 0
    baseOffset = 0
    while not baseY > baseHeight:
        baseX = 0
        while not baseX > baseWidth:
            subData = subImageData[matchOffset]
            baseData = baseImageData[baseOffset]
            matching = subData[0] == baseData[0] and subData[1] == baseData[1] and subData[2] == baseData[2]
            #print ("TEST {},{} - {} vs {}".format(baseY, baseX, baseOffset, matchOffset))

            if matching:
                #print ("FOUND {} {} - {} {}/{}".format(baseX, baseY, matchX, matchOffset, subMatchesNeeded))
                # Record the location of the first match
                if not matchOffset:
                    matchStartX = baseX
                    matchStartY = baseY
                    matchStartOffset = baseOffset

                matchOffset += 1
                if matchOffset == subMatchesNeeded:
                    return True

                matchX += 1
                if matchX == subWidth:
                    #print ("HOP {} {} - {}, {}".format(baseX, baseY, baseOffset, matchOffset))
                    baseOffset += baseWidth + matchStartX - baseX
                    baseX = matchStartX
                    baseY += 1
                    matchX = 0
                    #print ("TO {} {} - {}, {}".format(baseX, baseY, baseOffset, matchOffset))
                    continue

            # Reset on failed match
            elif matchOffset:
                #print ("MISS {} {} - {}, {}".format(baseX, baseY, baseOffset, matchOffset))
                baseX = matchStartX
                baseY = matchStartY
                matchX = 0
                matchOffset = 0
                baseOffset = matchStartOffset

            # Start new row when x is too far right
            elif baseX > lastUsableBaseX:
                baseOffset += baseWidth - baseX
                break

            # Kill when Y is too high
            elif baseY > lastUsableBaseY:
                baseY = baseHeight
                break

            baseX += 1
            baseOffset += 1

        baseY += 1

    return False

def main():
    window = _get_windows_bytitle('Snes9X')[0]
    win32gui.SetForegroundWindow(window)
    sleep(0.01)

    while True:
        start_time = time()

        #print ("screenshot")
        screenshot(window)

        #print ("match")
        resultsS = matchTemplate(Image.open('screenshot.bmp'), Image.open('state_player_select.bmp'))
        resultsE = matchTemplate(Image.open('screenshot.bmp'), Image.open('player_ehonda_left.bmp'))
        print("player select: {}".format(resultsS))
        print("ehonda face right: {}".format(resultsE))

        #end_time = time()

        #print("Process took {} seconds".format(end_time-start_time))

        sleep(0.2)

main()