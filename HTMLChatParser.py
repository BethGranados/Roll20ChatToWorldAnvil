#!/usr/bin/env python3
######################################
# Roll 20 chat scraper
# Made to make collecting dialogue easier.
######################################

from bs4 import *
import copy

class chatBlock:
    def __init__(self, new):
        self.textBlock = new
    def updateText(self, new):
        self.textBlock = new
    def printContents(self, time, speaker):
        print(self.textBlock)


class manualDiceRolls(chatBlock):
    def printContents(self, time, speaker):
        print("[quote]" + self.textBlock + "|" + speaker + ", " + time + "[/quote]")

class typedDialog(chatBlock):
    def printContents(self, time, speaker):
        print(time)
        print("[aloud]" + speaker + ": " + self.textBlock + "[/aloud]")

class emoteChat(chatBlock):
    def printContents(self, time, speaker):
        print(time)
        print("[aloud]" + self.textBlock + "[/aloud]")
class npcSave(chatBlock):
    def __init__(self, name, roll, math):
        self.sheetCharName = name
        self.rollType = roll
        self.diceMath = math
    def printContents(self, time, speaker):
        print("[quote]" + self.rollType + ": " + self.diceMath + "|" + self.sheetCharName + " (" + speaker + "), " + time + "[/quote]")
class npcSkillCheck(chatBlock):
    def __init__(self, rollString, rollType):
        self.roll = rollString
        self.type = rollType
    def printContents(self, time, speaker):
        print("[quote]" + self.roll + " " + self.type + "|" + speaker + " " + time + "[/quote]")

class npcAction(chatBlock):
    def __init__(self, name, roll, blurb):
        self.sheetCharName = name
        self.rollType = roll
        self.report = blurb
    def printContents(self, time, speaker):
        print("[quote]" + self.rollType + "[br]" + self.report + "|" + self.sheetCharName + " (" + speaker + "), " + time + "[/quote]")

class npcAttack(chatBlock):
    sheetCharName = ""
    title = ""
    report = ""
    def __init__(self, title, name, attack):
        self.sheetCharName = name
        self.title = title
        self.report = attack
    def printContents(self, time, speaker):
        print("[quote]" + self.title + " " + self.report + "[br]")
        print(self.sheetCharName + "|" + speaker + " " + time + "[/quote]")

class npcDamage(chatBlock):
    def __init__(self, title, attack, damType):
        self.damageType = damType
        self.title = title
        self.report = attack
    def printContents(self, time, speaker):
        print("[quote]" + self.title + " " + self.report + " " + self.damageType + "|" + speaker + " " + time + "[/quote]")

class pcFeatures(chatBlock):
    def __init__(self, title, rep, type = None):
        self.title = title
        self.type = type  
        self.report = rep
    def printContents(self, time, speaker):
        if(self.type):
            print("[quote]" + self.title + "[br]" + self.type + "[br]" + self.report.replace("\n", "[br]").replace("[br][br]", "[br]") + "[/quote]")
        else:
            print("[quote]" + self.title + "[br]" + self.report.replace("\n", "[br]").replace("[br][br]", "[br]") + "[/quote]")

class pcSpells(chatBlock):
    def __init__(self, title, schoolAndLevel, castTime, spellRange, components, report, spellSave):
        self.title = title
        self.schoolAndLevel = schoolAndLevel
        self.castTime = castTime
        self.spellRange = spellRange
        self.components = components
        self.report = report
        self.spellSave = spellSave
    def printContents(self, time, speaker):
        print("[quote]" + self.title + ", " + self.schoolAndLevel + "[br]Casting Time " + self.castTime + ", Range: " + self.spellRange + " Components: " + self.components + "[br]" + self.report + "[br]" + self.spellSave + "|" + speaker + ", " + time + "[/quote]")

class damageChat(chatBlock):
    def __init__(self, spellRange, rollString):
        self.spellRange = spellRange
        self.rollString = rollString
    def printContents(self, time, speaker):
        print(time)
        print("[quote]" + self.spellRange + ": " + self.rollString + "[/quote]")


class speakerSegment:

    def __init__(self, time, by):
       self.Time = time
       self.Speaker = by
       self.blocks = []

    def addBlock(self, chatBlock):
        self.blocks.append(chatBlock)
    def printBlockContents(self):
        for block in self.blocks:
            block.printContents(self.Time, self.Speaker)



def has_only_one_class(tag, class_name):
    return tag.has_attr('class') and len(tag['class']) == 1 and tag['class'][0] == class_name


def message_rollresult(div):
    message = ""
    rolling = div.find('div', class_="formula")
    message = message + rolling.text
    dicegrouping = div.find('div', class_="dicegrouping")
    message = message + "(" + dicegrouping.text.replace("\n", "").replace("(", "").replace(")", "") + ")"
    result = div.find('div', class_="rolled")
    message = message + "=" + result.text.replace("\n", "")
    newRollChat = manualDiceRolls(message)
    return newRollChat


def message_general(div):
    message = ""

    spelloutput = div.find('div', class_="sheet-rolltemplate-spelloutput")
    attack = div.find('div', class_="sheet-rolltemplate-atk")
    damage = div.find('div', class_="sheet-rolltemplate-dmg")

    simple = div.find('div', class_="sheet-rolltemplate-simple")

    
    traits = div.find('div', class_="sheet-rolltemplate-traits")
    npcaction = div.find('div', class_="sheet-rolltemplate-npcaction")
    npcatk = div.find('div', class_="sheet-rolltemplate-npcatk")
    npcdmg = div.find('div', class_="sheet-rolltemplate-npcdmg")
    dmgaction = div.find('div', class_="sheet-rolltemplate-dmgaction")
    spell = div.find('div', class_="sheet-rolltemplate-spell")

    npc = div.find('div', class_="sheet-rolltemplate-npc")

    if(spell):
        container = spell.find('div', class_="sheet-container")
        sheets = container.find_all('div', {'class':['sheet-title sheet-row', 'sheet-italics sheet-row', 'sheet-row', 'sheet-row sheet-spellsavedc']})
        for sheet in sheets:
            message = message + sheet.text

        newRollChat = chatBlock(message)
        return newRollChat
        
        
    elif(dmgaction):
        container = dmgaction.find('div', class_="sheet-container")
        sheets = container.find_all('div', {'class':['sheet-container', 'sheet-result', 'sheet-solo', 'sheet-label']})
        for sheet in sheets:
            message = message + sheet.text
        
        type = container.find('div', class_="sheet-row sheet-header")

        if(type):
            message = message + "Type: " + type.span.text.replace("\n", "")
        
        statBlock = container.find('div', class_="sheet-row sheet-subheader")

        if(statBlock):
            message = message + "NPC: " + statBlock.span.text.replace("\n", "")
        
        #noGoodName = npc.find('div', class_="sheet-row")
        noGoodName = container.find(lambda tag: has_only_one_class(tag, 'sheet-row'))

        if(noGoodName):
            message = message + "????: " + noGoodName.text.replace("\n", "")
        newRollChat = chatBlock(message)
        return newRollChat

    elif(npcdmg):
        container = npcdmg.find('div', class_="sheet-container")

        type = container.find('span', class_="sheet-italics sheet-translated")

        if(type):
            title = type.text.replace("\n", "")
        
        Numbers = container.find('span', class_="inlinerollresult")

        if(Numbers):
            attack = Numbers.text.replace("\n", "")
        
        for part in container.find_all("span", {'class':['sheet-italics sheet-translated', 'inlinerollresult']}): 
            part.decompose()
        damType = npcdmg.text.replace("\n", "").replace(" ", "")
        newRollChat = npcDamage(title, attack, damType)
        return newRollChat

    elif(npcatk):
        type = npcatk.find('div', class_="sheet-row sheet-header")

        if(type):
            title = type.text.replace("\n", "")
        
        statBlock = npcatk.find('div', class_="sheet-row sheet-subheader")

        if(statBlock):
            name = statBlock.span.text.replace("\n", "")
        
        noGoodName = npcatk.find(lambda tag: has_only_one_class(tag, 'sheet-row'))

        if(noGoodName):
            attack = noGoodName.text.replace("\n", "")
        newRollChat = npcAttack(title, name, attack)
        return newRollChat

    elif(npcaction):
        container = npcaction.find('div', class_="sheet-container")

        type = container.find('div', class_="sheet-row sheet-header")

        if(type):
            roll = type.span.text.replace("\n", "")
        
        statBlock = container.find('div', class_="sheet-row sheet-subheader")

        if(statBlock):
            name = statBlock.span.text.replace("\n", "")
        
        noGoodName = container.find(lambda tag: has_only_one_class(tag, 'sheet-desc'))

        if(noGoodName):
            blurb = noGoodName.text.replace("\n", "")
        newRollChat = npcAction(name, roll, blurb)
        return newRollChat

    elif(traits):
                
        type = traits.find('div', class_="sheet-row sheet-header")

        if(type):
            title = type.span.text.replace("\n", "").replace(":", "")
        
        statBlock = traits.find('div', class_="sheet-row sheet-subheader")

        if(statBlock):
            source = statBlock.span.text.replace("\n", "").replace(":", "")
        
        noGoodName = traits.find(lambda tag: has_only_one_class(tag, 'sheet-row'))

        if(noGoodName):
            rep = noGoodName.text
        if (statBlock):
            newRollChat = pcFeatures(title, rep, source)
        else:
            newRollChat = pcFeatures(title, rep)
        return newRollChat

    elif(simple):
        container = simple.find('div', class_="sheet-container")
        rolls = container.find_all('div', class_="sheet-adv")

        rollString = ""
        if (rolls):
            for roll in rolls:
               rollString = rollString + " " + roll.text.replace("\n", "")
        else:
            roll = container.find('div', class_="sheet-solo")
            rollString = rollString + roll.text.replace("\n", "")

        label = container.find('div', class_="sheet-label")
        rollType = label.text.replace("\n", "")
        newRollChat = npcSkillCheck(rollString, rollType)
        return newRollChat

    elif(npc):
        
        type = npc.find('div', class_="sheet-row sheet-header")

        if(type):
            math = type.span.text.replace("\n", "")
        

        statBlock = npc.find('div', class_="sheet-row sheet-subheader")

        if(statBlock):
            name = statBlock.span.text.replace("\n", "")
        
        #noGoodName = npc.find(lambda tag: has_only_one_class(tag, 'sheet-row'))
        noGoodName = npc.find('span', class_="inlinerollresult")

        if(noGoodName):
            rollType = noGoodName.text.replace("\n", "")

        newRollChat = npcSave(name,math,rollType)
        return newRollChat
            
    elif(spelloutput):
        container = spelloutput.find('div', class_="sheet-container")

        titleBlock = container.find('div', class_="sheet-title sheet-row")
        
        if(titleBlock):
            title = titleBlock.span.text

        spellTypeBlock = container.find('div', class_="sheet-italics sheet-row")
        
        if(spellTypeBlock):
            schoolAndLevel = spellTypeBlock.span.text

        sheet_rows = container.find_all(lambda tag: has_only_one_class(tag, 'sheet-row'))
        
        for part in sheet_rows:
            for spans in part.find_all("span", {'class':['sheet-bold']}): 
                spans.decompose()

        if(sheet_rows[0]):
            castTime = sheet_rows[0].span.text
        if(sheet_rows[1]):
            range = sheet_rows[1].span.text
        if(sheet_rows[2]):
            components = sheet_rows[2].span.text.replace("\n", "").replace(" ", "")
        if(sheet_rows[3]):
            report = sheet_rows[3].span.text

        saveDCBlock = container.find('div', class_="sheet-row sheet-spellsavedc")

        if(saveDCBlock):
            spellSave = saveDCBlock.text
        
        newRollChat = pcSpells(title, schoolAndLevel, castTime, range, components, report, spellSave)
        return newRollChat


    elif(attack):
        container = attack.find('div', class_="sheet-container")
        sheets = container.find_all('div', {'class':['sheet-solo', 'sheet-sublabel', 'sheet-label']})

        rolls = container.find_all('div', class_="sheet-adv")

        message = message + "Rolls: "
        if (rolls):
            for roll in rolls:
               message = message + roll.text.replace("\n", "")
        else:
            roll = container.find('div', class_="sheet-solo")
            message = message + roll.text.replace("\n", "")

        label = container.find('div', class_="sheet-label")
        message = message + "Label: "
        message = message + label.text.replace("\n", "")

        subLabel = container.find('div', class_="sheet-sublabel")

        if(subLabel):
            message = message + "Distance: "
            message = message + subLabel.text.replace("\n", "")
        newRollChat = chatBlock(message)
        return newRollChat
    
    elif(damage):

        sublabel = damage.find('div', class_="sheet-sublabel")

        if(sublabel):
            spellRange = sublabel.text.replace("\n", "")

        rolls = damage.find_all('div', class_="sheet-adv")

        rollString = ""
        if (rolls):
            for roll in rolls:
                #damTypeBlock = roll.find('span', class_="sheet-sublabel")
                #damType = damTypeBlock.text
                rollString = rollString + " " + roll.text.replace("\n", " ") #+ " " + damType
        else:
            roll = damage.find('div', class_="sheet-solo")
            damTypeBlock = roll.find('span', class_="sheet-sublabel")
            damType = damTypeBlock.text
            rollString = rollString + roll.text.replace("\n", " ") + " " + damType
            

        newRollChat = damageChat(spellRange, "")
        return newRollChat
    else:
        for part in div.find_all("span", {'class':['tstamp', 'by']}): 
            part.decompose()
        message = message + div.text
        newChat = typedDialog(div.text)
        return newChat

    




def message_emote(div):
    newRollChat = emoteChat(div.text)
    return newRollChat

f = open('Test.html', 'r')

content = f.read()

soup = BeautifulSoup(content, 'html.parser')

for div in soup.find_all("div", {'class':['spacer', 'sheet-spacer', 'sheet-advspacer', 'avatar', 'flyout', 'sheet-spelldesc-link', 'backing', 'clear', 'sheet-arrow-right']}): 
    div.decompose()

speakerList = []

#div = soup.find('div', class_='message general you')

#divs = soup.find_all('div', {'class':['message general you', 'message general', 'message emote']})

divs = soup.find_all('div', {'class':['message general you', 'message general', 'rollresult', 'message emote']})

for div in divs:
    tStamp = div.find('span', class_="tstamp")
    speaker = div.find('span', class_="by")

    if(tStamp and speaker):
        newSpeaker = speakerSegment(tStamp.text.replace(",", ""), speaker.text.replace(":", ""))
        speakerList.append(newSpeaker)

    if((len(div['class']) > 1) and (div['class'][1] == "emote")):
        newChat = message_emote(div)
        speakerList[-1].addBlock(newChat)
        continue

    if((len(div['class']) > 1) and (div['class'][1] == "general")):
        newChat = message_general(div)
        speakerList[-1].addBlock(newChat)
        continue

    if((len(div['class']) > 1) and (div['class'][1] == "rollresult")):
        newChat = message_rollresult(div)
        speakerList[-1].addBlock(newChat)
        continue
    


for speaker in speakerList:
    speaker.printBlockContents()


