#!/usr/bin/env python3

import chatblock


class attackDamageChat(chatblock.chatBlock):
    def __init__(self, attackName, attackRoll, spellRange, rollString, damageImplement, sheetdesc):
        self.attackName = attackName
        self.attackRoll = attackRoll
        self.spellRange = spellRange
        self.rollString = rollString
        self.damageImplement = damageImplement
        self.sheetdesc = sheetdesc
    def printContents(self, time, speaker):

        blockText = "[quote]"
        
        emptyLine = True

        if (self.attackRoll):
            blockText += self.attackRoll + " "
            emptyLine = False
        
        if (self.attackName):
            blockText += self.attackName + " "
            emptyLine = False

        if (self.damageImplement):
            blockText += self.damageImplement + " "
            emptyLine = False

        if (emptyLine == False):
            blockText += "[br]"
            emptyLine = True

        if (self.sheetdesc):
            blockText += self.sheetdesc + " "
            emptyLine = False

        if (emptyLine == False):
            blockText += "[br]"
            emptyLine = True

        if (self.rollString):
            blockText += self.rollString + " "
            emptyLine = False

        blockText += "|"+ speaker + ", " + time + "[/quote]"
        print(blockText)
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)