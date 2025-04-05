#!/usr/bin/env python3
######################################
# Roll 20 chat scraper
# Made to make collecting dialogue easier.
######################################
import dataextractionmethods, speakersegment

from bs4 import *
import sys


def usage():
  print("usage: HTMLChatParser.py Filename [DEBUG]")


# Sanity checks in case Beth typos
arg_nums = len(sys.argv)

if arg_nums <= 1:
  print("Not enough arguments!") 
  usage()
  sys.exit()

if sys.argv[1] == "-h":
    usage()
    sys.exit()

if arg_nums > 2:
    debug = sys.argv[2]
else:
    debug = 0

f = open(sys.argv[1], 'r')

content = f.read()

soup = BeautifulSoup(content, 'html.parser')

# Clean up fluff elements from HTML
for div in soup.find_all("div", {'class':['spacer', 'sheet-spacer', 'sheet-advspacer', 'avatar', 'flyout', 'sheet-spelldesc-link', 'backing', 'clear', 'sheet-arrow-right']}): 
    div.decompose()

speakerList = []

divs = soup.find_all('div', {'class':['message general you', 'message general', 'rollresult', 'message emote']})

for div in divs:
    tStamp = div.find('span', class_="tstamp")
    speaker = div.find('span', class_="by")

    if(tStamp and speaker):
        newSpeaker = speakersegment.speakerSegment(tStamp.text.replace(",", ""), speaker.text.replace(":", ""))
        speakerList.append(newSpeaker)
    elif (len(speakerList) == 0):
        newSpeaker = speakersegment.speakerSegment("2:00", "???")
        speakerList.append(newSpeaker)

    if((len(div['class']) > 1) and (div['class'][1] == "emote")):
        newChat = dataextractionmethods.dataExtractionMethods.message_emote(div, debug)
        speakerList[-1].addBlock(newChat)
        continue

    if((len(div['class']) > 1) and (div['class'][1] == "general")):
        newChat = dataextractionmethods.dataExtractionMethods.message_general(div, debug)
        speakerList[-1].addBlock(newChat)
        continue

    if((len(div['class']) > 1) and (div['class'][1] == "rollresult")):
        newChat = dataextractionmethods.dataExtractionMethods.message_rollresult(div, debug)
        speakerList[-1].addBlock(newChat)
        continue

for speaker in speakerList:
    speaker.printBlockContents()
