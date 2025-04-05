#!/usr/bin/env python3

import chatblock

class npcSkillCheck(chatblock.chatBlock):
    def __init__(self, rollString, rollType):
        self.roll = rollString
        self.type = rollType
    def printContents(self, time, speaker):
        print("[quote]" + self.roll + " " + self.type + "|" + speaker + " " + time + "[/quote]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)