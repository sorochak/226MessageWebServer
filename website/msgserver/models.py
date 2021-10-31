from django.db import models
import msgserver.constants
from django.core.exceptions import ValidationError

#
# PURPOSE:
# Validates to ensure a key is alphanumeric and length of key equals KEYLENGTH
#
# PARAMETERS:
# 'key' contains the key field of a Message instance
#
# RETURN/SIDE EFFECTS:
# Raises a validation error if key is not alphanumeric or does not equal KEYLENGTH.
#

def validate_key(key):
    if len(key) != msgserver.constants.KEYLENGTH or not key.isalnum():
        raise ValidationError('Invalid Key', code='key_value')

#
# PURPOSE:
# Validates to ensure a message is greater than or equal to MINMSGLENGTH or less than or equal to MAXMSGLENGTH
#
# PARAMETERS:
# 'msg' contains the message field of a Message instance
#
# RETURN/SIDE EFFECTS:
# Raises a validation error if msg is less than MINMSGLENGTH or  greater than MAXMSGLENGTH.
#

def validate_msg_length(msg):
    if len(msg) < msgserver.constants.MINMSGLENGTH or len(msg) > msgserver.constants.MAXMSGLENGTH:
        raise ValidationError('Invalid Message Length', code='message_value')

#
# PURPOSE:
# Validates to ensure a key is not duplicated
#
# PARAMETERS:
# 'k' contains the key field of a Message instance
#
# RETURN/SIDE EFFECTS:
# Raises a validation error if k is found to duplicate a key already in the database.
#

def validate_unique_key(k):
    for message in Message.objects.all():
        if message.key == k:
            raise ValidationError('Key taken', code='duplicate key')

#
# PURPOSE:
# Defines a Message model
#
# PARAMETERS:
# 'models.Model' contains Django's Model class
#
# RETURN/SIDE EFFECTS:
# Creates a Message instance in the database.
#

class Message(models.Model):
    key = models.CharField(max_length= msgserver.constants.KEYLENGTH, validators=[validate_key, validate_unique_key])
    message = models.CharField(max_length= msgserver.constants.MAXMSGLENGTH, validators=[validate_msg_length])

    #
    # PURPOSE:
    # Returns the string representation of a Message instance
    #
    # PARAMETERS:
    # 'self' contains the Message instance.
    #
    # RETURN/SIDE EFFECTS:
    # Returns the string representation of the Message instance 'self'.
    #
    def __str__(self):
        return self.key + ' : ' + self.message