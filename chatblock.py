#!/usr/bin/env python3

class chatBlock:
    def __init__(self, new):
        self.textBlock = new
    def updateText(self, new):
        self.textBlock = new
    def printContents(self, time, speaker):
        print(self.textBlock)
    def setDebug(self, debug):
        self.debug = debug
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)