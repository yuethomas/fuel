# Create your views here.
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import auth
from fuel.models import FuelUser, Profile, Record
from django.core.urlresolvers import reverse

def index(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('home'))

# requires not logged in
def login(request):

    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        return render_index(request)

    elif 'email' in request.POST and 'password' in request.POST:
       
        user = auth.authenticate(username=request.POST['email'], password=request.POST['password'])

        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render_index(request, login_fail=True)
    
    else:
        return render_index(request, login_fail=True)

#add record
def addrecord(request):
    t = Record();
    t.user=request.user;
    #print request.GET['date'];
    #t.date = request.GET['date'];
    t.steps = request.GET['step']
    t.calories = request.GET['calories']
    t.fuelscore = request.GET['fuel_score']
    print 'aaaaa'
    #t.save_amount();
    t.save()
    print 'dddd'
    #request.user.get_profile().save();

# requires logged in
def home(request):
    t = loader.get_template('home.html')
    c = RequestContext(request, {'username': request.user.get_full_name()})
    return HttpResponse(t.render(c))  
    #return HttpResponse('%s <a href="/logout/">logout</a>'%request.user.get_full_name())

# requires logged in; logs out
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))
    
