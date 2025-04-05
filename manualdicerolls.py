#!/usr/bin/env python3

import chatblock

class manualDiceRolls(chatblock.chatBlock):
    def printContents(self, time, speaker):
        print("[quote]" + self.textBlock + "|" + speaker + ", " + time + "[/quote]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)