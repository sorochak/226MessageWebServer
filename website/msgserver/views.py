from msgserver.models import Message
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
import json

#
# PURPOSE:
# Filters the database for a specific key and returns a Web Response that contains the key and associated message.
#
# PARAMETERS:
# 'request' contains a Web Request
# 'key' contains an alphanumeric key used to identify a message.
#
# RETURN/SIDE EFFECTS:
# Returns a Web Response that contains a key and associated message.
#

def get_message(request,key):
    message = Message.objects.filter(key=key)
    if (len(message) == 1):
        return HttpResponse("%(key)s: %(message)s" % { 'key':message[0].key, 'message':message[0].message})
    else:
        return HttpResponse("")

#
# PURPOSE:
# Returns a Web Response that contains all messages in JSON format.
#
# PARAMETERS:
# 'request' contains a Web Request.
#
# RETURN/SIDE EFFECTS:
# Returns a Web Response that contains all messages in JSON format.
#

def index(request):
    return HttpResponse(json.dumps(list(Message.objects.all()), cls=MessageEncoder))

#
# PURPOSE:
# A class based generic view for a form to complete a database insertion
#
# PARAMETERS:
# 'CreateView' contains a view that displays a form for creating a Message object.
#
# RETURN/SIDE EFFECTS:
# Upon successful database insertion, calls the index view.
#

class MessageCreate(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('index')

#
# PURPOSE:
# A class based generic view for a form to update a previous database insertion
#
# PARAMETERS:
# 'UpdateView' contains a view that updates an instance of a Message object.
#
# RETURN/SIDE EFFECTS:
# Upon successful object update, calls the index view.
#

class MessageUpdate(UpdateView):
    model = Message
    fields = ['message']
    success_url = reverse_lazy('index')

    #
    # PURPOSE:
    # override of Django's get_object view, this method retrieves the object
    #
    # PARAMETERS:
    # 'self' contains the object being created.
    #
    # RETURN/SIDE EFFECTS:
    # returns the object associated with a key.
    #
    def get_object(self):
        return Message.objects.get(key=self.kwargs.get("key"))

#
# PURPOSE:
# A class based view for encoding classes to JSON format
#
# PARAMETERS:
# 'json.JSONEncoder' contains an extensible JSON encoder for Python data structures.
#
# RETURN/SIDE EFFECTS:
# calls a function that returns an instance of a Message encoded to JSON.
#

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return { 'key' : obj.key, 'message' : obj.message }
        return json.JSONEncoder.default(self, obj)
