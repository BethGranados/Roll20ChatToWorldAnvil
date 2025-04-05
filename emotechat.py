#!/usr/bin/env python3

import chatblock

class emoteChat(chatblock.chatBlock):
    def printContents(self, time, speaker):
        print(time)
        print("[aloud]" + self.textBlock + "[/aloud]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)