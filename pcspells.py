#!/usr/bin/env python3

import chatblock

class pcSpells(chatblock.chatBlock):
    def __init__(self, title, schoolAndLevel, castTime, spellRange, components, report, spellSave, spellImplement, target, duration, higherLevelBlurb, forDesc):
        self.title = title
        self.schoolAndLevel = schoolAndLevel
        self.castTime = castTime
        self.spellRange = spellRange
        self.components = components
        self.report = report
        self.spellSave = spellSave
        self.spellImplement = spellImplement
        self.target = target
        self.duration = duration
        self.higherLevelBlurb = higherLevelBlurb
        self.forDesc = forDesc
    def printContents(self, time, speaker):
        blockText = "[quote]"
        
        emptyLine = True
        
        if (self.title):
            blockText += self.title
            emptyLine = False
        
        if (self.schoolAndLevel):
            if(emptyLine == False):
                blockText += ", "
            blockText += self.schoolAndLevel + " "

        if (emptyLine == False):
            blockText += "[br]"
            emptyLine = True

        if(self.castTime):
            blockText += "Casting Time: " + self.castTime + " "
            emptyLine = False
        
        if(self.spellRange):
            blockText += "Range: " + self.spellRange + " "
            emptyLine = False

        if(self.components):
            blockText += "Components: " + self.components
            emptyLine = False   

        if (emptyLine == False):
            blockText += "[br]"
            emptyLine = True
        
        if (self.report):
            blockText += self.report + "[br]"

        if (emptyLine == False):
            blockText += "[br]"
            emptyLine = True

        if (self.higherLevelBlurb):
            blockText += self.higherLevelBlurb + "[br]"

        if (self.spellSave):
            blockText += self.spellSave

        blockText += "|" + speaker + ", " + time + "[/quote]"
        

        print(blockText)

    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)