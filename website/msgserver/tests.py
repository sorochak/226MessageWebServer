from django.test import TestCase
from msgserver.models import Message
import msgserver.constants

# Create your tests here.

class MessageTestCase(TestCase):
    def test_create(self):
        response = self.client.post("/msgserver/create/", { 'key':'87654321', 'message':"Testing Create Message!"})
        m = Message.objects.get(key='87654321')
        self.assertEqual(m.key, "87654321")
        self.assertEqual(m.message, "Testing Create Message!")

    def test_duplicate(self):
        response = self.client.post("/msgserver/create/", { 'key':'87654321', 'message':"Testing Create Message!"})
        response = self.client.post("/msgserver/create/", { 'key':'87654321', 'message':"Testing Create Message!"})

        self.assertFormError(response, 'form', 'key', 'Key taken') 
        
        try:
           msg = Message.objects.filter(key='87654321')
           if(len(msg) != 1):
            self.fail()
        except Message.DoesNotExist:
            pass   

    def test_key_length(self):
        response = self.client.post("/msgserver/create/", { 'key':'12345', 'message':"Testing Key Length!"})
        self.assertFormError(response, 'form', 'key', 'Invalid Key') 

    def test_key_alNum(self):
        response = self.client.post("/msgserver/create/", { 'key':'12345$$$', 'message':"Testing Key alnum!"})
        self.assertFormError(response, 'form', 'key', 'Invalid Key') 
    
    def test_msg_length(self):
        msg = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis viverra odio. Donec vehicula nisi ligula, quis rutrum turpis tempor ac. Integer mi nisi vivamus.'
        response = self.client.post("/msgserver/create/", { 'key':'88888888', 'message':msg})
        self.assertFormError(response, 'form', 'message', 'Ensure this value has at most ' + str(msgserver.constants.MAXMSGLENGTH) + ' characters (it has ' + str(len(msg)) + ').')

    def test_update(self):
        k = '87654321'
        k2 = '88888888'
        updatedMsg = "Message was updated!"
        response = self.client.post("/msgserver/create/", { 'key':k2, 'message':"Test Object!"})
        response = self.client.post("/msgserver/create/", { 'key':k, 'message':"Testing Update Message!"})
        response = self.client.post(f"/msgserver/update/{k}/", { 'key':k, 'message':updatedMsg})

        m = Message.objects.filter(key=k)[0]
        self.assertEqual(m.message, updatedMsg)


    def test_retrJSON(self):
        k1 = '87654321'
        k2 = '88888888'
        response = self.client.post("/msgserver/create/", { 'key':k1, 'message':"Test Object1"})
        response = self.client.post("/msgserver/create/", { 'key':k2, 'message':"Test Object2"})

        reply = self.client.get("/msgserver/")

        self.assertEqual(reply.content, b'[{"key": "87654321", "message": "Test Object1"}, {"key": "88888888", "message": "Test Object2"}]')

        print(reply.content)

        
