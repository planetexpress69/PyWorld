# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Person
#from django.contrib.auth.models import User
#from tastypie.models import ApiKey
import datetime

def listusers(request, message = ''):
    


    #for user in User.objects.all():
        #ApiKey.objects.create(user=user)
    
    user_list = Person.objects.all().order_by('created')
    
    return render_to_response(
                              'list.html',
                              { 'user_list' : user_list,
                                'message' : message },
                              context_instance = RequestContext(request)
                              )


def newuser(request, message = ''):
    
    headline = "New user"
    
    user = Person()
    
    return render_to_response('form.html',
                              {'action' : 'add',
                               'button' : 'Add',
                               'message' : message,
                               'headline' : headline,
                               'user' : user,
                               },
                              context_instance = RequestContext(request))
    
        
def edituser(request, pid):
    
    headline = "Edit user"
    
    try:
        Person.objects.get(id=pid)
        
    except Person.DoesNotExist:
        return listusers(request, message = 'User does not exists')
    
    user = Person.objects.get(id=pid)
    
    return render_to_response('form.html',
                              {'action' : 'update/' + pid,
                               'user' : user,
                               'button' : 'Update',
                               'headline' : headline },
                              context_instance = RequestContext(request))
    
def adduser(request):
    
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    
    if (first_name == "") or (last_name == ""):
        return newuser(request, message = 'Input must not be empty')
        
    
    person = Person(
                    first_name = first_name,
                    last_name = last_name,
                    created = datetime.datetime.now(),
                    modified = datetime.datetime.now(),
                    )
    person.save()
    
    # should be redirect instead
    return listusers(request, message = 'User added')


def updateuser(request, pid):
    
    try:
        Person.objects.get(id=pid)
        
    except Person.DoesNotExist:
        return listusers(request, message = 'User does not exists')
    
    user = Person.objects.get(id=pid)
    
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    
    user.first_name = first_name
    user.last_name = last_name
    user.modified = datetime.datetime.now()
    
    user.save()
    
    # should be redirect instead
    return listusers(request, message = 'User updated')


def deleteuser(request, pid):
    
    try:
        Person.objects.get(id=pid)
        
    except Person.DoesNotExist:
        return listusers(request, message = 'User does not exists')
    
    person = Person.objects.get(id=pid)
    person.delete()
    
    # should be redirect instead
    return listusers(request, message = 'User deleted')