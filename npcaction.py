#!/usr/bin/env python3

import chatblock

class npcAction(chatblock.chatBlock):
    def __init__(self, name, roll, blurb):
        self.sheetCharName = name
        self.rollType = roll
        self.report = blurb
    def printContents(self, time, speaker):
        print("[quote]" + self.rollType + "[br]" + self.report + "|" + self.sheetCharName + " (" + speaker + "), " + time + "[/quote]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)