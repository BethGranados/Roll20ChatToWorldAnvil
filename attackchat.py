#!/usr/bin/env python3

import chatblock

class attackChat(chatblock.chatBlock):
    sheetCharName = ""
    title = ""
    report = ""
    def __init__(self, title, name, attack):
        self.sheetCharName = name
        self.title = title
        self.report = attack
    def printContents(self, time, speaker):
        print("[quote]" + self.report + " " + self.title)
        print("|" + self.sheetCharName + "(" + speaker + ")" + " " + time + "[/quote]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)