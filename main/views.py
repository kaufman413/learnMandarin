from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from main.models import Prompt, Lesson, UserProfile, Story, Response

import random

def index(request):
    # get name and points from userProfile

    if request.user.is_authenticated:
        print("is authenticated")
        username = request.user.username
        points = UserProfile.objects.filter(username=username)[0].points
    else:
        print("is not authenticated")
        username = "NOBODY"
        points = 0
    #logout(request)
    lessons = Lesson.objects.all()
    return render(request, 'main/home.html', {"lessons": lessons, "username":username, "points":points})


def lesson(request, number):

    #get name and points from userProfile
    username = request.user.username
    try:
        points = UserProfile.objects.filter(username=username)[0].points
    except:
        points = 0


    n_learnWords = 10
    lesson = Lesson.objects.filter(number=number)[0]
    words = lesson.phrase_set.all()
    learnWords = [] # [audio,thingToGuess,option1,option2,answer] (answer=1|2)
    #random number for the word to be test,
    #random number for the word to be used as an option which != original word
    #random number for the type of test that it is [char->pinyin, pinyin->char, english->char, char->english]
    print(words[0].characters)
    for i in range(n_learnWords):
        testWord = words[random.randint(0,len(words)-1)]
        decoyWord = testWord
        while decoyWord == testWord:
            decoyWord = words[random.randint(0,len(words)-1)]
        testType = random.randint(2,3)
        if testType == 0: #char->pinyin
            if random.randint(1,2) == 1: learnWords.append([testWord.audio, testWord.characters, testWord.pinyin, decoyWord.pinyin, 1])
            else: learnWords.append([testWord.audio, testWord.characters, decoyWord.pinyin, testWord.pinyin, 2])
        elif testType == 1: #pinyin->char
            if random.randint(1, 2) == 1: learnWords.append([testWord.audio, testWord.pinyin, testWord.characters, decoyWord.characters, 1])
            else: learnWords.append([testWord.audio, testWord.pinyin, decoyWord.characters, testWord.characters, 2])
        elif testType == 2: #english->char
            if random.randint(1, 2) == 1: learnWords.append([testWord.audio, testWord.english, testWord.characters, decoyWord.characters, 1])
            else: learnWords.append([testWord.audio, testWord.english, decoyWord.characters, testWord.characters, 2])
        elif testType == 3: #char->english
            if random.randint(1, 2) == 1: learnWords.append([testWord.audio, testWord.characters, testWord.english, decoyWord.english, 1])
            else: learnWords.append([testWord.audio, testWord.characters, decoyWord.english, testWord.english, 2])


    return render(request, 'main/lesson.html', {"lesson":lesson, "words":words, "learnWords":learnWords, "username":username, "points":points})



def questions(request, number):
    # get name and points from userProfile
    username = request.user.username
    try:
        points = UserProfile.objects.filter(username=username)[0].points
    except: points = 0
    story = Story.objects.filter(name=number)[0]
    responses = Response.objects.filter(storyId = number)
    prompts = Prompt.objects.filter(storyId=number)
    vars = story.vars.split(",")
    return render(request, 'main/questions.html', {"story":story, "responses":responses, "vars":vars, "prompts":prompts, "username":username, "points":points})


def logoff(request):
    logout(request)
    return redirect("/")


@csrf_exempt
def ajaxPractice(request, username, amount):
    user = UserProfile.objects.filter(username=username)[0]

    user.points += int(amount)
    user.save()

    return HttpResponse("hi")



















"""
if not request.user.is_authenticated:
    try:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            lessons = Lesson.objects.all()
            return render(request, 'main/home.html', {"lessons": lessons})
        else:
            return render(request, 'homepage/loginUser.html', {})
    except:
        return render(request, '', {})
else:
    logout(request)
    lessons = Lesson.objects.all()
    return render(request, 'main/home.html', {"lessons": lessons})


if not request.user.is_authenticated:
    print('hiiiiiii')
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
print("authentication")
print(request.user.is_authenticated)
username = request.POST['username']
password = request.POST['password']

user = authenticate(username=username, password=password)

if user is not None:
    login(request, user)
    lessons = Lesson.objects.all()
    return render(request, 'main/home.html', {"lessons": lessons})
else:
    return render(request, 'homepage/loginUser.html', {})
"""