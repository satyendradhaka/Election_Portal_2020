from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Voter
from .forms import CaptchaTestForm
from functools import wraps

def captcha_required(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    captcha = request.session.get('human',False)
    if not captcha:
        return redirect('captcha')
    else:
        return function(request, *args, **kwargs)    
  return wrap

def verify(request):
    if request.method=="POST":
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            request.session['human'] = True
            return redirect('vote')
    else:
        form = CaptchaTestForm()

    return render(request, 'captchaVerify.html', {'form': form})

@captcha_required
def vote(request):
    #have to make the voting function ##### Alan451
    print(request.user.username)
    username = request.user.username
    if Voter.objects.filter(username=username).exists():
        return HttpResponse('u are a verified voter, proceed')
    else:
        return HttpResponse('get out of here')
        