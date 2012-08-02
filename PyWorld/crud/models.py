# Create your models here.

from django.db import models

class Person(models.Model):
    #attributes
    first_name = models.TextField()
    last_name = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    
    
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    