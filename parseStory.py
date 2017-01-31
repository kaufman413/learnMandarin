import sys
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = "learnMandarin.settings"
django.setup()

from main.models import Prompt,Response, Story


file = sys.argv[1]
storyName = file.split("_")[-1].split(".")[0]

with open(file, "r") as f:
    story = f.read().split('\n')

#we want to create a dictionary for the variables
tab = ""#'\t'
vars = {}
storyStart = -1
promptIdCounter = 1
csvVars = "" # for passing to the Story in the format "x,y,z"
#first get the tab and variables
for i in range(len(story)):
    if story[i][:3] == "tab":
        tabLine = story[i].split()
        if tabLine[0] != "tab" or tabLine[1] != "=":
            #print("error with tab line, must be (for example): tab = \\t")
            exit()
        tab = tabLine[2]
        if tab == "tab": tab = "\t"
    elif story[i][:4] == "vars":
        varsLine = story[i].split()
        if varsLine[0] != "vars" or varsLine[1] != "=":
            #print("error with vars line, must be (for example): vars = x,y,z")
            exit()
        csvVars = varsLine[2]
        varNames = varsLine[2].split(",")
        for varName in varNames:
            vars[varName] = ""

        storyStart = i+1
        break


story = story[storyStart:]
if '' in story: story.remove('')

#takes a promptText (a list of the lines) as input and
#returns a prompt object
def parsePrompt(chunk):
    global tab, vars, storyName, promptIdCounter

    #print(chunk)
    #find the offset, and then change the chunk to a standard form
    offset = 0
    for c in chunk[0]:
        if c == tab:
            offset += 1
        else: break

    #standardize
    for i in range(len(chunk)):
        chunk[i] = chunk[i][offset:]

    #print(chunk)

    prompt = Prompt(promptText=chunk[0], storyId=storyName, option1="", promptId=promptIdCounter)
    promptIdCounter += 1
    prompt.save()

    #starting with first line of first option, iterate through the lines
    for j in range(1, len(chunk)):
        line = chunk[j]
        #print(line)

        # check if the line is set off by a tab
        # if not, then we found an option
        if line[0] != tab and prompt.option1 == "":
            #set the option1 for the prompt to this line
            prompt.option1 = line
            #then create the response object
            option1 = Response(storyId=storyName, option1or2="1", previousPrompt=prompt, ifStatement="")
            print("response created for option1", option1)
            option1.save()
            optionsToPassUp1 = [option1]
            #now we start from what comes under the option
            #these sublines will be offset by 1 tab
            k = j+1
            for notk in range(j+1, len(chunk)):
                subline = chunk[k]
                #print("subline1",[subline.split()])
                #if there is no tab, then we have reached the end
                if subline[0] != tab:
                    #print('move on')
                    break
                #this means that we have found the nextPrompt
                elif subline[1] == tab:
                    #print('go deeper')
                    countForNextPrompt = 0
                    for l in range(k, len(chunk) +1):
                        #print(chunk[l])
                        # the nextPrompt will be in atleast 2 deep, anything shallower is not a part of it
                        if l == len(chunk) or chunk[l][1] != tab:
                            #print(k,l)
                            option1.nextPrompt, subOptionsToPassUp1 = parsePrompt(chunk[k:l])
                            print("retrieved response from deeper option1")
                            optionsToPassUp1.pop(-1)
                            optionsToPassUp1.extend(subOptionsToPassUp1)
                            #print(optionsToPassUp1)
                            #print("returned up")
                            k = l-1
                            #print("option1: ",option1)
                            option1.save()
                            break
                #if statement
                elif subline[1:3] == "if" and subline[-1] == ":":
                    if option1.ifStatement == "":
                        option1.ifStatement = subline[1:]
                    else:
                        option1.save()
                        option1 = Response(storyId=storyName, option1or2="1", previousPrompt=prompt)
                        print("created an if response for options 1", option1)
                        option1.ifStatement = subline[1:]
                        option1.save()
                        optionsToPassUp1.append(option1)
                #set variable statement
                elif len(subline[1:].split()) > 2 and subline[1:].split()[1] == ":=" and subline.split()[0][1:] in vars:
                    option1.setVariable = subline[1:]
                #otherwise, it's (hopefully) the response text, if any
                else:
                    #print("response text: ",subline)
                    option1.responseText = subline[1:]
                k+=1
                if k >= len(chunk): break
            option1.save()

        #for option 2
        elif line[0] != tab and prompt.option1 != "":
            #set the option2 for the prompt to this line
            prompt.option2 = line
            #then create the response object
            option2 = Response(storyId=storyName, option1or2="2", previousPrompt=prompt, ifStatement="")
            print("response created for option2", option2)
            option2.save()
            optionsToPassUp2 = [option2]
            #now we start from what comes under the option
            #these sublines will be offset by 1 tab
            k = j+1
            for notk in range(j+1, len(chunk)):
                subline = chunk[k]
                #print("subline2",[subline.split()])
                #if there is no tab, then we have reached the end
                if subline[0] != tab:
                    #print('move on')
                    break
                #this means that we have found the nextPrompt
                elif subline[1] == tab:
                    print('go deeper')
                    print(chunk)
                    countForNextPrompt = 0
                    for l in range(k, len(chunk) +1):
                        #print(chunk[l])
                        # the nextPrompt will be in atleast 2 deep, anything shallower is not a part of it
                        if l == len(chunk) or chunk[l][1] != tab:
                            #print(k,l)
                            option2.nextPrompt, subOptionsToPassUp2 = parsePrompt(chunk[k:l])
                            print("retrieved response from deeper option2")
                            optionsToPassUp2.pop(-1)
                            optionsToPassUp2.extend(subOptionsToPassUp2)
                            #print(optionsToPassUp2)
                            print("returned up")
                            k = l-1
                            #print("option1: ",option1)
                            option2.save()
                            break
                #if statement
                elif subline[1:3] == "if" and subline[-1] == ":":
                    if option2.ifStatement == "":
                        option2.ifStatement = subline[1:]
                    else:
                        option2.save()
                        option2 = Response(storyId=storyName, option1or2="2", previousPrompt=prompt)
                        print("created an if response for options 2", option2)
                        option2.ifStatement = subline[1:]
                        option2.save()
                        optionsToPassUp2.append(option2)
                #set variable statement
                elif len(subline[1:].split()) > 2 and subline[1:].split()[1] == ":=" and subline.split()[0][1:] in vars:
                    option2.setVariable = subline[1:]
                #otherwise, it's (hopefully) the response text, if any
                else:
                    #print("response text: ",subline)
                    option2.responseText = subline[1:]
                k+=1
                if k >= len(chunk): break
            option2.save()



    prompt.save()
    optionsToPassUp2.extend(optionsToPassUp1)
    return prompt, optionsToPassUp2




#then split up the story into the outer prompts

promptTexts = []

countForPrompts = 0
previousPromptIndex = 0

for i in range(len(story)):
    line = story[i]
    if line[0] != tab or i == len(story)-1:
        if i == len(story)-1: i += 1 #this is to get the last line in
        countForPrompts += 1
        if (countForPrompts-1) % 3 == 0 and countForPrompts != 1:
            promptTexts.append(story[previousPromptIndex:i])
            previousPromptIndex = i


#print(promptTexts)

#first parse the first chunk
prompt, oldOptions = parsePrompt(promptTexts[0])

#then create a Story
story = Story(firstPrompt=prompt, vars=csvVars, name=storyName)
story.save()

for promptText in promptTexts[1:]:
    prompt, newOptions = parsePrompt(promptText)
    for option in oldOptions:
        option.nextPrompt = prompt
        option.save()
    oldOptions = newOptions









"""words to use:
tab = \t
vars = pet, food, drink
你好, I want to 买 a pet, but I won't have much time or 钱 to take care of it. Can you help me?
	1. 买狗！
	Hmmm, a 狗？Okay..
	pet := 狗
	2. 买猫！
	A 猫？That seems like a 好 idea.
	pet := 猫
Okay, now I need to get something for it to 喝. There's 牛奶 and 水. Which should I get?
	1. 买水！
	好, 水seems less expensive.
	drink := 水
	2. 买牛奶！
	I think cats like 牛奶..
	drink := 牛奶
		Do you like to 喝牛奶?
		1. I love to 喝牛奶！
		2. 喝牛奶？Maybe if I were a 牛..
One more thing, I need to get something for it to 吃. Should I 买饭 or 买鱼？
	1. 饭很好！
	food := 饭
	2. 鱼很好！
	food := 鱼
好, so I bought a ${pet}, some ${drink} for it to 喝, and some ${food} for it to 吃.

if vars == 猫，牛奶，鱼:
	My 猫loves the 牛奶 and 鱼 and I love my 猫！But I don't quite have enough 钱 to sustain its habits..\nWill you give me some 钱？
		1. I don't have 钱 for you!
		Understandable..
		+20exp
		2. Sure.
		谢谢，thanks!
		+50exp
if vars == 猫:
	I love my 猫！
	+30exp
if vars == 狗，牛奶，鱼:
	I like my 狗, but I don't quite have enough time or 钱. Especially while feeding it 牛奶 and 鱼.
	+5exp
if vars == 狗:
	It's a cool 狗, I just don't have much time for it..
	+20exp"""