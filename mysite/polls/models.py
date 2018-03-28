from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    # You can use an optional first positional argument to a Field to designate a human-readable name. That’s used in a couple of
    # introspective parts of Django, and it doubles as documentation. If this field isn’t provided, Django will use the machine-readable name.
    # In this example, we’ve only defined a human-readable name for Question.pub_date. For all other fields in this model,
    # the field’s machine-readable name will suffice as its human-readable name.

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
