#!/usr/bin/env python3

import chatblock


class damageChat(chatblock.chatBlock):
    def __init__(self, spellRange, rollString, sheetLabel):
        self.spellRange = spellRange
        self.rollString = rollString
        self.sheetLabel = sheetLabel
    def printContents(self, time, speaker):
        output = "[quote]"

        emptyLine = True

        if(self.sheetLabel):
            output += self.sheetLabel
            emptyLine = False

        if(self.rollString):
            if (emptyLine == False):
                blockText += "[br]"
            output += self.rollString

        if(self.spellRange):
            if (emptyLine == False):
                blockText += "[br]"
            output += self.spellRange

        output += "|"+ speaker + ", " + time + "[/quote]"
        print(output)
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)