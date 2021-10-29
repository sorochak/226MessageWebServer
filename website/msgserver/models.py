from django.db import models
import msgserver.constants
from django.core.exceptions import ValidationError

# Create your models here.

def validate_key(key):
    if len(key) != msgserver.constants.KEYLENGTH or not key.isalnum():
        raise ValidationError('Invalid Key', code='key_value')

def validate_msg_length(msg):
    if len(msg) < msgserver.constants.MINMSGLENGTH or len(msg) > msgserver.constants.MAXMSGLENGTH:
        raise ValidationError('Invalid Message Length', code='message_value')

def validate_unique_key(k):
    for message in Message.objects.all():
        if message.key == k:
            raise ValidationError('Key taken', code='duplicate key')


class Message(models.Model):
    key = models.CharField(max_length= msgserver.constants.KEYLENGTH, validators=[validate_key, validate_unique_key])
    message = models.CharField(max_length= msgserver.constants.MAXMSGLENGTH, validators=[validate_msg_length])

    def __str__(self):
        return self.key + ' : ' + self.message