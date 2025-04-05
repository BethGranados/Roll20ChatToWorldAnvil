#!/usr/bin/env python3

import chatblock

class npcSave(chatblock.chatBlock):
    def __init__(self, name, roll, math):
        self.sheetCharName = name
        self.rollType = roll
        self.diceMath = math
    def printContents(self, time, speaker):
        print("[quote]" + self.rollType + ": " + self.diceMath + "|" + self.sheetCharName + " (" + speaker + "), " + time + "[/quote]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)