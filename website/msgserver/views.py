from msgserver.models import Message
from django.http import HttpResponse


def get_message(request,key):
    message = Message.objects.filter(key=key)
    return HttpResponse("%(key)s: %(message)s" % { 'key':message[0].key, 'message':message[0].message})
    
