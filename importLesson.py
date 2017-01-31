import sys
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = "learnMandarin.settings"
django.setup()

from main.models import Lesson, Phrase

file = sys.argv[1]
lessonNumber = file.split("_")[-1].split(".")[0]

#read in the file
with open(file, "r") as f:
    lesson = f.read().split("\n")
if '' in lesson: lesson.remove('')

lessonObject = Lesson(number=lessonNumber)

#extract the text, points, and name to create the lesson
for line in lesson[:3]:
    if line[:5].lower() == "text:":
        text = line[5:].strip()
        print("text:",text)
        lessonObject.text = text
    elif line[:7].lower() == "points:":
        points = int(line[7:].strip())
        print("points:",points)
        lessonObject.points = points
    elif line[:5].lower() == "name:":
        name = line[5:].strip()
        print("name:",name)
        lessonObject.name = name
    else:
        print("error with first three lines. they should look something like this: Text: In this lesson you will learn about drinks.\nPoints: 100\nName: none\n ABORTING")
        exit()
lessonObject.save()

#the file will be a list of the words as such english,pinyin,characters
for word in lesson[3:]:
    print(word)
    word = word.split(",")
    english,pinyin,characters = word[0],word[1],word[2]
    newPhrase = Phrase(english=english,pinyin=pinyin,characters=characters,type="phrase",lesson=lessonObject)
    newPhrase.save()


#example
"""
Text: In this lesson you will learn about drinks.
Points: 100
Name: none
water,shuǐ,水
alcohol,jiǔ,酒
tea,chá,茶
coffee,kāfēi,咖啡
beer,píjiǔ,啤酒
red wine,hóngjiǔ,红酒
white wine,báijiǔ,白酒
"""
