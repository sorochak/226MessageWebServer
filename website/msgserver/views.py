from msgserver.models import Message
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
import json


def get_message(request,key):
    message = Message.objects.filter(key=key)
    return HttpResponse("%(key)s: %(message)s" % { 'key':message[0].key, 'message':message[0].message})

def index(request):
    return HttpResponse(json.dumps(list(Message.objects.all()), cls=MessageEncoder))


class MessageCreate(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('index')

class MessageUpdate(UpdateView):
    model = Message
    fields = ['message']
    success_url = reverse_lazy('index')

    def get_object(self):
        return Message.objects.get(key=self.kwargs.get("key"))
   

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return { 'key' : obj.key, 'message' : obj.message }
        return json.JSONEncoder.default(self, obj)
