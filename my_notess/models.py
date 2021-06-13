from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    #A topic that a user would like to create notes about
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        #Return string representation of the model
        return self.text

class Note(models.Model):
    #A specific note regarding a topic
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #Return string representation of the model
        return f"{self.text[:50]}..."
