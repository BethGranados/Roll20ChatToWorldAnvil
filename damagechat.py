#!/usr/bin/env python3

import chatblock


class damageChat(chatblock.chatBlock):
    def __init__(self, spellRange, rollString):
        self.spellRange = spellRange
        self.rollString = rollString
    def printContents(self, time, speaker):
        print("[quote]" + self.spellRange + ": " + self.rollString + "[/quote]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)