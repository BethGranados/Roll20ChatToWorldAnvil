#!/usr/bin/env python3

class speakerSegment:
    def __init__(self, time, by):
       self.Time = time
       self.Speaker = by
       self.blocks = []
    def addBlock(self, chatBlock):
        self.blocks.append(chatBlock)
    def printBlockContents(self):
        for block in self.blocks:
            block.printDebug()
            block.printContents(self.Time, self.Speaker)
