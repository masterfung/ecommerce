from django.db import models

# Create your models here.
class Contact(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self, ):
        return "Message from: " + str(self.email)