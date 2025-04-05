#!/usr/bin/env python3

import chatblock


class pcFeatures(chatblock.chatBlock):
    def __init__(self, title, rep, type = None):
        self.title = title
        self.type = type  
        self.report = rep
    def printContents(self, time, speaker):
        if(self.type):
            print("[quote]" + self.title + "[br]" + self.type + "[br]" + self.report.replace("\n", "[br]").replace("[br][br]", "[br]") + "[/quote]")
        else:
            print("[quote]" + self.title + "[br]" + self.report.replace("\n", "[br]").replace("[br][br]", "[br]") + "[/quote]")
    def printDebug(self):
        if self.debug != 0:
            print(__class__.__name__)