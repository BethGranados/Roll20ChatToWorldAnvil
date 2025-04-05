#!/usr/bin/env python3

import chatblock


class npcFullAttack(chatblock.chatBlock):
    sheetCharName = ""
    title = ""
    report = ""
    def __init__(self, title, name, attack,rolls,description,damage):  
        self.sheetCharName = name
        self.title = title
        self.report = attack
        self.rolls = rolls
        self.description = description
        self.damage = damage
    def printContents(self, time, speaker):
        
        blockText = "[quote]" + self.title + " " + self.report
        blockText = blockText + "|" + self.sheetCharName + "(" + speaker + ")" + " " + time + "[/quote]"

        
        blockText = blockText + "\n" + "[quote]"
        

        if (self.rolls):
            blockText += self.rolls

        if (self.description):
            blockText += "[br]" + self.description

        blockText += "|"+ self.sheetCharName + "(" + speaker + "), " + time + "[/quote]"

        print(blockText)

    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)