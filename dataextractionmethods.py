#!/usr/bin/env python3

# The ugly one!

import manualdicerolls, emotechat, npcattack, npcdamage, chatblock, pcfeatures, npcskillcheck, npcsave, pcspells, damagechat, attackdamagechat, typeddialog, npcaction, npcfullattack, attackchat, dmgaction
import re

class dataExtractionMethods:
    def has_only_one_class(tag, class_name):
        return tag.has_attr('class') and len(tag['class']) == 1 and tag['class'][0] == class_name

    def message_emote(div, debug):
        newRollChat = emotechat.emoteChat(div.text)
        newRollChat.setDebug(debug)
        return newRollChat

    def message_rollresult(div, debug):
        message = ""
        rolling = div.find('div', class_="formula")
        message = message + rolling.text
        dicegrouping = div.find('div', class_="dicegrouping")
        if(dicegrouping):
            message = message + "(" + dicegrouping.text.replace("\n", "").replace("(", "").replace(")", "") + ")"
        result = div.find('div', class_="rolled")
        message = message + "=" + result.text.replace("\n", "")
        newRollChat = manualdicerolls.manualDiceRolls(message)
        newRollChat.setDebug(debug)
        return newRollChat


    def message_general(div, debug):
        message = ""

        spelloutput = div.find('div', class_="sheet-rolltemplate-spelloutput")
        attack = div.find('div', class_="sheet-rolltemplate-atk")
        attackDamage = div.find('div', class_="sheet-rolltemplate-atkdmg")
        damage = div.find('div', class_="sheet-rolltemplate-dmg")

        simple = div.find('div', class_="sheet-rolltemplate-simple")

        
        traits = div.find('div', class_="sheet-rolltemplate-traits")
        npcactions = div.find('div', class_="sheet-rolltemplate-npcaction")
        npcatk = div.find('div', class_="sheet-rolltemplate-npcatk")
        npcdmg = div.find('div', class_="sheet-rolltemplate-npcdmg")
        daction = div.find('div', class_="sheet-rolltemplate-dmgaction")
        spell = div.find('div', class_="sheet-rolltemplate-spell")

        npc = div.find('div', class_="sheet-rolltemplate-npc")

        npcfattack = div.find('div', class_="sheet-rolltemplate-npcfullatk")

        if(spell):
            container = spell.find('div', class_="sheet-container")
            sheets = container.find_all('div', {'class':['sheet-title sheet-row', 'sheet-italics sheet-row', 'sheet-row', 'sheet-row sheet-spellsavedc']})
            for sheet in sheets:
                message = message + re.sub(" +", " ", sheet.text)
                message = re.sub("\n ", "\n", message)
                message = re.sub("\n+", "\n", message)

            newRollChat = chatblock.chatBlock("[aloud]" + message + "[/aloud]")
            newRollChat.setDebug(debug)
            return newRollChat
            
            
        elif(daction):
            npcName = ""
            label = ""
            container = daction.find('div', class_="sheet-container")

            type = container.find('div', class_="sheet-row sheet-header")

            if(type):
                label = type.span.text.replace("\n", "")
            
            statBlock = container.find('div', class_="sheet-row sheet-subheader")

            if(statBlock):
                npcName = statBlock.span.text.replace("\n", "")
            
            #noGoodName = npc.find('div', class_="sheet-row")
            descriptionBlock = container.find(lambda tag: dataExtractionMethods.has_only_one_class(tag, 'sheet-row'))

            if(descriptionBlock):
                description = descriptionBlock.text.replace("\n", "")

            dmgActionChat = dmgaction.dmgAction(npcName,label,"")
            dmgActionChat.setDebug(debug)
            return dmgActionChat

        elif(npcdmg):
            info = ""
            container = npcdmg.find('div', class_="sheet-container")

            titleBlock = container.find('span', class_="sheet-italics sheet-translated")

            if(titleBlock):
                title = titleBlock.text.replace("\n", "")
            
            Numbers = container.find('span', class_="inlinerollresult")

            if(Numbers):
                attack = Numbers.text.replace("\n", "")
            
            for part in container.find_all("span", {'class':['sheet-italics sheet-translated', 'inlinerollresult']}): 
                part.decompose()



            damType = Numbers.text.replace("\n", "")
            #damType = re.sub(" +", " ", damType)
            
            infoBlock = npcdmg.find(lambda tag: dataExtractionMethods.has_only_one_class(tag, 'sheet-row'))
            if(infoBlock):
                info = infoBlock.span.text
            newRollChat = npcdamage.npcDamage(title, attack, damType, info)
            newRollChat.setDebug(debug)
            return newRollChat

        elif(npcatk):
            type = npcatk.find('div', class_="sheet-row sheet-header")

            if(type):
                title = type.text.replace("\n", "")
            
            statBlock = npcatk.find('div', class_="sheet-row sheet-subheader")

            if(statBlock):
                name = statBlock.span.text.replace("\n", "")
            
            noGoodName = npcatk.find(lambda tag: dataExtractionMethods.has_only_one_class(tag, 'sheet-row'))

            if(noGoodName):
                attack = noGoodName.text.replace("\n", "").replace("|", "")
            newRollChat = npcattack.npcAttack(title, name, attack)
            newRollChat.setDebug(debug)
            return newRollChat

        elif(npcactions):
            container = npcactions.find('div', class_="sheet-container")

            type = container.find('div', class_="sheet-row sheet-header")

            if(type):
                roll = type.span.text.replace("\n", "")
            
            statBlock = container.find('div', class_="sheet-row sheet-subheader")

            if(statBlock):
                name = statBlock.span.text.replace("\n", "")
            
            noGoodName = container.find(lambda tag: dataExtractionMethods.has_only_one_class(tag, 'sheet-desc'))

            if(noGoodName):
                blurb = noGoodName.text.replace("\n", "")
            newRollChat = npcaction.npcAction(name, roll, blurb)
            newRollChat.setDebug(debug)
            return newRollChat

        elif(traits):
                    
            type = traits.find('div', class_="sheet-row sheet-header")

            if(type):
                title = type.span.text.replace("\n", "").replace(":", "")
            
            statBlock = traits.find('div', class_="sheet-row sheet-subheader")

            if(statBlock):
                source = statBlock.span.text.replace("\n", "").replace(":", "")
            
            noGoodName = traits.find(lambda tag: dataExtractionMethods.has_only_one_class(tag, 'sheet-row'))

            if(noGoodName):
                rep = noGoodName.text
            if (statBlock):
                newRollChat = pcfeatures.pcFeatures(title, rep, source)
            else:
                newRollChat = pcfeatures.pcFeatures(title, rep)
            newRollChat.setDebug(debug)
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
            newRollChat = npcskillcheck.npcSkillCheck(rollString, rollType)
            newRollChat.setDebug(debug)
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

            newRollChat = npcsave.npcSave(name,math,rollType)
            newRollChat.setDebug(debug)
            return newRollChat
                
        elif(spelloutput):
            spellImplement = ""
            report = ""
            target = ""
            title = ""
            schoolAndLevel = "" 
            castTime = "" 
            range = "" 
            components = "" 
            spellSave = "" 
            spellImplement = "" 
            duration = "" 
            higherLevelBlurb = ""
            forDesc = ""


            container = spelloutput.find('div', class_="sheet-container")

            forDescBlock = container.find('div', class_="sheet-title sheet-desconly sheet-row")

            if (forDescBlock):
                forDesc = forDescBlock.span.text

            titleBlock = container.find('div', class_="sheet-title sheet-row")

            if(titleBlock):
                title = titleBlock.span.text
                spellImplementBlock = titleBlock.find('span', class_="sheet-grey")
                if (spellImplementBlock):
                    spellImplement = spellImplementBlock.text


            spellTypeBlock = container.find('div', class_="sheet-italics sheet-row")
            
            if(spellTypeBlock):
                schoolAndLevel = spellTypeBlock.span.text

            sheet_rows = container.find_all(lambda tag: dataExtractionMethods.has_only_one_class(tag, 'sheet-row'))
            
            #for part in sheet_rows:
            #    for spans in part.find_all("span", {'class':['sheet-bold']}): 
            #        spans.decompose()

            for part in sheet_rows:
                partLabelBlock = part.find("span", {'class':['sheet-bold']})
                if (partLabelBlock):
                    partLabel = partLabelBlock.text
                    partLabelBlock.decompose()
                    match partLabel:
                        case "Casting Time:":
                            castTime = part.span.text
                        case "Range:":
                            range = part.span.text
                        case "Components:":
                            components = part.span.text.replace("\n", "").replace(" ", "")
                        case "Target:":
                            target = part.span.text
                        case "Duration:":
                            duration = part.span.text
                        case "At Higher Levels":
                            higherLevelBlurb = part.span.text
                        case _:
                            print(part)


            #report = sheet_rows[3].span.text

            reportBlock = container.find('span', class_="sheet-description")
            if(reportBlock):
                report = reportBlock.text

            saveDCBlock = container.find('div', class_="sheet-row sheet-spellsavedc")

            if(saveDCBlock):
                spellSave = saveDCBlock.text
            
            newRollChat = pcspells.pcSpells(title, schoolAndLevel, castTime, range, components, report, spellSave, spellImplement, target, duration, higherLevelBlurb, forDesc)
            newRollChat.setDebug(debug)
            return newRollChat


        elif(attack):
            Title = ""
            Attack = ""
            Name = ""
            container = attack.find('div', class_="sheet-container")
            sheets = container.find_all('div', {'class':['sheet-solo', 'sheet-sublabel', 'sheet-label']})

            rolls = container.find_all('div', class_="sheet-adv")

            if (rolls):
                for roll in rolls:
                    Attack = Attack + roll.text.replace("\n", "")
            else:
                AttackBlock = container.find('div', class_="sheet-solo")
                if(AttackBlock):
                    Attack = Attack + AttackBlock.text.replace("\n", "")

            label = container.find('div', class_="sheet-label")
            Title = label.text.replace("\n", "")

            #subLabel = container.find('div', class_="sheet-sublabel")

            #if(subLabel):
            #    distance = subLabel.text.replace("\n", "")
            
            
            attackC = attackchat.attackChat(Title,"Name", Attack)
            attackC.setDebug(debug)
            return attackC
        
        elif(damage):
            spellRange = ""
            sublabel = damage.find('div', class_="sheet-sublabel")
            stuff = ""

            if(sublabel):
                spellRange = sublabel.span.text.replace("\n", "")

            sheetLabel = damage.find('class', class_="sheet-label")

            if(sheetLabel):
                stuff = sheetLabel.span.text

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
                #damType = damTypeBlock.text
                rollString = rollString + roll.text.replace("\n", " ")
                

            newRollChat = damagechat.damageChat(spellRange, rollString, stuff)
            newRollChat.setDebug(debug)
            return newRollChat
        
        elif(attackDamage):
            attackRoll = ""
            spellRange = ""
            rollString = ""
            damageImplement = ""
            moveName = ""
            desc = ""

            moveNameBlock = attackDamage.find('div', class_="sheet-label")
            if(moveNameBlock):
                
                damageImplementBlock = moveNameBlock.find('span', class_="sheet-grey")
                if(damageImplementBlock):
                    damageImplement = damageImplementBlock.text.strip(',').strip()
                    damageImplementBlock.decompose()
                moveName = moveNameBlock.span.text.replace("\n", " ").replace("\t", "")
                moveName = re.sub(" +", " ", moveName)
            
            
            attackRollBlock = attackDamage.find('div', class_="sheet-container sheet-atk")

            if(attackRollBlock):
                inlineBlock = attackRollBlock.find('span', class_="inlinerollresult")
                if(inlineBlock):
                    attackRoll = inlineBlock.text

            descBlock = attackDamage.find('div', class_="sheet-desc")
            
            if(descBlock):
                desc = descBlock.text
                desc = desc.replace("\n", " ").replace("\t", "")
                desc = re.sub(" +", " ", desc).strip()

            ######

            rolls = attackDamage.find_all('div', class_="sheet-adv")
            
            if (rolls):
                for roll in rolls:
                    rollString = rollString + " " + roll.text.replace("\n", " ") #+ " " + damType
            else:
                damType = ""
                rollBlock = attackDamage.find('div', class_="sheet-solo")
                damTypeBlock = rollBlock.find('span', class_="sheet-sublabel")
                if(damTypeBlock):
                    damType = damTypeBlock.text
                    damTypeBlock.decompose()
                rollString = rollBlock.span.text.replace("\n", " ") + " " + damType

            if(rollString):
                rollString = rollString.replace("  ", " ").strip()

            #####
            container = attackDamage.find('div', class_="sheet-container sheet-damagetemplate")

            RangeBlock = container.find('div', class_="sheet-sublabel")

            if(RangeBlock):
                spellRange = RangeBlock.text.replace("\n", " ")
            #####
            newRollChat = attackdamagechat.attackDamageChat(moveName, attackRoll, spellRange, rollString, damageImplement, desc)
            newRollChat.setDebug(debug)
            return newRollChat

        elif(npcfattack):
            weapon = ""
            pcname = ""
            attack = ""
            rollStats = ""
            description = ""
            rolls = ""

            container = npcfattack.find('div', class_="sheet-container")


            thing1 = container.find('div', class_="sheet-row sheet-header")
            if(thing1):
                weapon = thing1.span.text
                weapon = re.sub(" +", " ", weapon).strip()
                weapon = re.sub("\n", " ", weapon).strip()

            thing2 = container.find('div', class_="sheet-row sheet-subheader")
            if(thing2):
                pcname = thing2.span.text
                pcname = re.sub(" +", " ", pcname).strip()
                pcname = re.sub("\n", " ", pcname).strip()

            thing3 = container.find(lambda tag: dataExtractionMethods.has_only_one_class(tag, 'sheet-row'))
            
            if(thing3):
                attack = thing3.text
                attack = re.sub(" +", " ", attack).strip()
                attack = re.sub("\n", " ", attack).strip()

            damageContainer = npcfattack.find('div', class_="sheet-container sheet-dmgcontainer sheet-damagetemplate")
            
            if(damageContainer):
                damageBlock = damageContainer.find('span', class_="sheet-italics sheet-translated")

                if(damageBlock):
                    damage = damageBlock.text
                    damage = re.sub(" +", " ", damage).strip()
                    damage = re.sub("\n", " ", damage).strip()
                    damageBlock.decompose()
                descriptionBlock = damageContainer.find('div', class_="sheet-row")
                
                if(descriptionBlock):
                    description = descriptionBlock.span.text
                    description = re.sub(" +", " ", description).strip()
                    description = re.sub("\n", " ", description).strip()
                    descriptionBlock.decompose()

                rolls = damageContainer.text
                rolls = re.sub(" +", " ", rolls).strip()
                rolls = re.sub("\n", " ", rolls).strip()
                

            newFullAttack = npcfullattack.npcFullAttack(weapon,pcname,attack,rolls,description,damage)
            newFullAttack.setDebug(debug)
            return newFullAttack
        else:
            for part in div.find_all("span", {'class':['tstamp', 'by']}): 
                part.decompose()
            message = message + div.text
            message = re.sub(" +", " ", message).strip()
            newChat = typeddialog.typedDialog(message)
            newChat.setDebug(debug)
            return newChat

    