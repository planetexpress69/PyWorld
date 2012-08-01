# crud/api.py
from django.contrib.auth.models import User, Group
from tastypie.authentication import BasicAuthentication,Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.exceptions import BadRequest
from django.db import models, IntegrityError
from tastypie.models import create_api_key
from tastypie.resources import ModelResource, ALL
from models import Person

class CreateUserResource(ModelResource):
    class Meta:
        resource_name = 'user'
        allowed_methods = ['post']
        object_class = User
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False
        fields = ['username']
        

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(CreateUserResource, self).obj_create(bundle, request, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save() 
            user = User.objects.get(id=bundle.obj.id)
            group = Group.objects.get(id=1)
            user.groups.add(group)
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle
    
    
    
    
    '''g = Group.objects.get(name='groupname') 
g.user_set.add(your_user)'''

'''
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        list_allowed_methods = ['get', 'post', 'put']
        allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        '''
        
class PersonResource(ModelResource):
    class Meta:
        queryset = Person.objects.all()
        resource_name = 'persons'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        models.signals.post_save.connect(create_api_key, sender=User)
        filtering = {
            'first_name' : ALL,
            'last_name' : ALL,
        }
        ordering = ['first_name', 'last_name', 'created', 'modified']