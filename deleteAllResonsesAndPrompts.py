import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = "learnMandarin.settings"
django.setup()

from main.models import Prompt,Response

prompts = Prompt.objects.all()
responses = Response.objects.all()

for prompt in prompts:
    prompt.delete()
for response in responses:
    response.delete()