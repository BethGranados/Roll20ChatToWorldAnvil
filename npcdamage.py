#!/usr/bin/env python3

import chatblock


class npcDamage(chatblock.chatBlock):
    def __init__(self, title, attack, damType, info):
        self.damageType = damType
        self.title = title
        self.report = attack
        self.info = info
    def printContents(self, time, speaker):

        blockText = "[quote]"
        
        emptyLine = True

        if (self.title):
            blockText += self.title + " "
            emptyLine = False
        
        if (self.report):
            blockText += self.report + " "
            emptyLine = False

        if (self.damageType):
            blockText += self.damageType + " "
            emptyLine = False

        if (emptyLine == False and self.info):
            blockText += "[br]" + self.info

        blockText += "|"+ speaker + ", " + time + "[/quote]"
        print(blockText)

    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)