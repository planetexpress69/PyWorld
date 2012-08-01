from django.conf.urls.defaults import patterns, include
from crud.views import listusers, newuser, adduser, edituser, updateuser, deleteuser
from crud.api import PersonResource, CreateUserResource
from tastypie.api import Api

#person_resource = PersonResource()
v1_api = Api(api_name='v1')
v1_api.register(PersonResource())
v1_api.register(CreateUserResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HelloDjangoWorld.views.home', name='home'),
    # url(r'^HelloDjangoWorld/', include('HelloDjangoWorld.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^/*$', listusers),
    (r'^new/*$', newuser),
    (r'^add/*$', adduser),
    (r'^edit/(?P<pid>\d+)', edituser),
    (r'^update/(?P<pid>\d+)', updateuser),
    (r'^delete/(?P<pid>\d+)', deleteuser),
    (r'^api/', include(v1_api.urls)),    
)
