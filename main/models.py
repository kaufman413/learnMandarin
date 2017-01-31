from django.db import models

# Create your models here.

class Phrase(models.Model):
    english =      models.CharField(max_length = 500)
    characters =   models.CharField(max_length = 500)
    pinyin =       models.CharField(max_length = 500)
    audio =        models.CharField(max_length = 500, default="none")
    type =         models.CharField(max_length = 6, choices = (('phrase','phrase'),('question','question'))) #either "phrase" or "test"
    picture =      models.CharField(max_length = 500, default="none")
    POS =          models.CharField(max_length = 100, default="none")
    semanticType = models.CharField(max_length = 100, default="none")
    response1 =    models.CharField(max_length = 25 , default="none")
    response2 =    models.CharField(max_length = 25 , default="none")
    lesson       = models.ForeignKey('Lesson', null=True, blank=True)

    def __str__(self):
        return self.english+" / "+self.characters

class Lesson(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=200, default="none")
    text = models.TextField()
    points =        models.IntegerField()

    def __str__(self):
        if self.name == "none":
            return "Lesson " + str(self.number)
        else:
            return "Lesson " + str(self.number) + " (%s)" % self.name



class UserProfile(models.Model):
    username = models.CharField(max_length=20)
    points = models.IntegerField()
    wordsExposedTo = models.TextField()
    progressOnLessons = models.TextField()

    def __str__(self):
        return self.username


#classes used for Interactive Stories
class Story(models.Model):
    name = models.CharField(max_length=100)
    firstPrompt = models.ForeignKey('Prompt', related_name="firstPrompt")
    vars = models.TextField();

    def __str__(self):
        return self.name

class Prompt(models.Model):
    storyId = models.CharField(max_length=100)
    promptId = models.CharField(max_length=3)
    #comingFromResponse = models.ForeignKey('Response', null=True, blank=True)
    promptText = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    vars = models.TextField()

    def __str__(self):
        return self.promptText

class Response(models.Model):
    storyId = models.CharField(max_length=100)
    option1or2 = models.CharField(max_length=1)
    ifStatement = models.TextField()
    responseText = models.TextField()
    setVariable = models.TextField() #this includes setting experience points at the end
    previousPrompt = models.ForeignKey('Prompt', null=True, related_name="previousPrompt")
    nextPrompt = models.ForeignKey('Prompt', null=True, related_name="nextPrompt")

    def __str__(self):
        try:
             if self.option1or2 == "1":
                 return self.previousPrompt.promptText[:20] + " / " + self.option1or2 + " " + self.previousPrompt.option1 + " / " + self.responseText
             elif self.option1or2 == "2":
                 return self.previousPrompt.promptText[:20] + " / " + self.option1or2 + " " + self.previousPrompt.option2 + " / " + self.responseText
        except:
            return "independent response"