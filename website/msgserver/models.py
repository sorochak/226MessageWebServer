from django.db import models

# Create your models here.

class Message(models.Model):
    key = models.CharField(max_length=8)
    message = models.CharField(max_length=160)

    def __str__(self):
        return self.key + ' : ' + self.message