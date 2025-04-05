#!/usr/bin/env python3

import chatblock

class typedDialog(chatblock.chatBlock):
    def printContents(self, time, speaker):
        print(time)
        print("[aloud]" + speaker + ": " + self.textBlock + "[/aloud]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)
