# crud/api.py
from django.contrib.auth.models import User, Group
from tastypie.authentication import BasicAuthentication,Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.exceptions import BadRequest
from django.db import models, IntegrityError
from tastypie.models import create_api_key, ApiKey
from tastypie.resources import ModelResource, ALL
from models import Person
import logging

logging.basicConfig()
logger = logging.getLogger('foo')


#user create resource
class CreateUserResource(ModelResource):
    
    class Meta:
        resource_name = 'user'
        allowed_methods = ['post']
        object_class = User
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False
        fields = ['username']
        models.signals.post_save.connect(create_api_key, sender=User)        

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(CreateUserResource, self).obj_create(bundle, request, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save() 
            # make user a member of group 'members'
            group = Group.objects.get(name='members')
            bundle.obj.groups.add(group)
            
            #by the way: this is how to fetch the apikey
            apikey = ApiKey.objects.get(user=bundle.obj)
            
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle

#record entity    
class PersonResource(ModelResource):
    
    class Meta:
        queryset = Person.objects.all()
        resource_name = 'persons'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        
        filtering = {
            'first_name' : ALL,
            'last_name' : ALL,
        }
        ordering = ['first_name', 'last_name', 'created', 'modified']