from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Voter,Contestant
from .forms import CaptchaTestForm
from functools import wraps
from datetime import datetime
import time
from django.contrib.auth import logout

def captcha_required(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    captcha = request.session.get('human',False)
    if not captcha:
        return redirect('captcha')
    else:
        return function(request, *args, **kwargs)    
  return wrap

def is_valid(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        username = request.user.username
        if Voter.objects.all().filter(username=username).exists():
            voter = Voter.objects.get(username=username)
            if voter.final_submit:
                return HttpResponse('u have already voted')
            else:
                return function(request, *args, **kwargs) 
        else:
            return HttpResponse('get out of here')

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
@is_valid
def voteCountModifier(dicti):
    vote_string=''
    vote_string += 'vp: '+str(dicti['vp'])+","
    print(vote_string)
    vote_string += 'hab: '+str(dicti['hab'])+","
    print(vote_string)
    vote_string += 'tech: ' +str(dicti['tech'])+","
    print(vote_string)
    vote_string += 'cult: '+str(dicti['cult'])+","
    print(vote_string)
    vote_string += 'sports: '+str(dicti['sports'])+","
    print(vote_string)   
    vote_string += 'welfare: '+str(dicti['welfare'])+","
    print(vote_string)   
    vote_string += 'sail: '+str(dicti['sail'])+","
    print(vote_string) 
    vote_string += 'swc: '+str(dicti['swc'])+","
    print(vote_string)
    if dicti['bsen']['nota']:
        vote_string += 'bsen: NOTA,'      
    else:
        vote_string+= 'bsen: {'
        for i in range(7):
            key = 'choice'+str(i+1)
            if dicti['bsen'][key] is not None:
                vote_string += str(dicti['bsen'][key])+","
                print(vote_string)
        vote_string += '},'
    if dicti['gsen']['nota']:
        vote_string += 'gsen: NOTA,'             
    else:
        vote_string+= 'gsen: {'
        for i in range(3):
            key = 'choice'+str(i+1)
            if dicti['gsen'][key] is not None:
                vote_string += str(dicti['gsen'][key])+","
                print(vote_string)
        vote_string += '},'
    return vote_string

@captcha_required
@is_valid             
def getMeSelectedCandidates(dicti):
    selectedCandidates = []
    if not dicti['vp'] == 'NOTA':
        selectedCandidates.append(('vp',Contestant.objects.get(pk=dicti['vp'])))
    else:
        selectedCandidates.append(('vp','NOTA')) 
    if not dicti['hab'] == 'NOTA':
        selectedCandidates.append(('hab',Contestant.objects.get(pk=dicti['hab'])))
    else:
        selectedCandidates.append(('hab','NOTA'))    
    if not dicti['tech'] == 'NOTA':
        selectedCandidates.append(('tech',Contestant.objects.get(pk=dicti['tech'])))
    else:
        selectedCandidates.append(('tech','NOTA'))
    if not dicti['cult'] == 'NOTA':
        selectedCandidates.append(('cult',Contestant.objects.get(pk=dicti['cult'])))
    else:
        selectedCandidates.append(('cult','NOTA'))
    if not dicti['sports'] == 'NOTA':
        selectedCandidates.append(('sports',Contestant.objects.get(pk=dicti['sports'])))
    else:
        selectedCandidates.append(('sports','NOTA'))    
    if not dicti['welfare'] == 'NOTA':
        selectedCandidates.append(('welfare',Contestant.objects.get(pk=dicti['welfare'])))
    else:
        selectedCandidates.append(('welfare','NOTA'))    
    if not dicti['sail'] == 'NOTA':
        selectedCandidates.append(('sail',Contestant.objects.get(pk=dicti['sail'])))
    else:
        selectedCandidates.append(('sail','NOTA'))    
    if not dicti['swc'] == 'NOTA':
        selectedCandidates.append(('swc',Contestant.objects.get(pk=dicti['swc'])))
    else:
        selectedCandidates.append(('swc','NOTA'))    
    if dicti['bsen']['nota']:
        selectedCandidates.append(('bsen','NOTA'))
    else:
        choice = []
        for i in range(7):
            key = 'choice'+str(i+1)
            if dicti['bsen'][key] is not None:
                choice.append((key,Contestant.objects.get(pk=dicti['bsen'][key])))
        selectedCandidates.append(('bsen',choice))
    if dicti['gsen']['nota']:
        selectedCandidates.append(('gsen','NOTA'))
    else:
        choice = []
        for i in range(3):
            key = 'choice'+str(i+1)
            if dicti['gsen'][key] is not None:
                choice.append((key,Contestant.objects.get(pk=dicti['gsen'][key])))
        selectedCandidates.append(('gsen',choice))
        
    return selectedCandidates

@captcha_required
@is_valid
def vote(request):
    dicti=request.session.get('option',{
        'vp': None,
        'hab':None,
        'tech':None,
        'cult':None,
        'welfare':None,
        'sports':None,
        'sail':None,
        'swc':None,
        'bsen':{
            'choice1':None,
            'choice2':None,
            'choice3':None,
            'choice4':None,
            'choice5':None,
            'choice6':None,
            'choice7':None,
            'done':False,
            'nota':False,
        },
        'gsen':{
            'choice1':None,
            'choice2':None,
            'choice3':None,
            'done':False,
            'nota':False,
        },
        
    })
    print(dicti)
    voter = Voter.objects.get(username=request.user.username)
    post= None
    if dicti['vp'] is None:
        post = 'vp'
    elif dicti['hab'] is None:
        post = 'hab'
    elif dicti['tech'] is None:
        post = 'tech'
    elif dicti['cult'] is None:
        post = 'cult'
    elif dicti['welfare'] is None:
        post = 'welfare'
    elif dicti['sports'] is None:
        post = 'sports'
    elif dicti['sail'] is None:
        post = 'sail'
    elif dicti['swc'] is None:
        post = 'swc'
    elif not dicti['bsen']['done']:
        post = 'bsen'    
        if voter.category == '0' or voter.category == '2':
            dicti['gsen']['done'] = True
            request.session['option']=dicti
    elif not dicti['gsen']['done']:
        post = 'gsen'

    if post is None:
        selectedCandidates = getMeSelectedCandidates(dicti)
        if request.method == "POST":
            if request.POST['choice'] == "done":
                voter.final_submit = True
                vote_string=voteCountModifier(dicti)
                #encrypt the string using our function
                voter.vote_string = vote_string
                voter.vote_time = datetime.now()
                voter.save()
                return HttpResponse("done")
            elif request.POST['choice'] == "bsen" or request.POST['choice'] == "gsen":
                dicti[request.POST['choice']]['done']=False
                if request.POST['choice']=="bsen":
                    leng = 7
                else:
                    leng = 3
                for i in range(leng):
                    key = 'choice'+str(i+1)
                    dicti[request.POST['choice']][key]=None
                request.session['option']=dicti
                return redirect('vote')
            else:
                dicti[request.POST['choice']]=None
                request.session['option']=dicti
                return redirect('vote')
        return render(request,'review.html',{'selectedCandidates':selectedCandidates})
    elif post == 'vp':
        contestantList = Contestant.objects.all().filter(post='VP').order_by('?')
        if request.method == "POST":
            dicti['vp']=request.POST['choice']
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'vote.html',{'contestantList':contestantList})
    elif post == 'hab':
        contestantList = Contestant.objects.all().filter(post='HAB').order_by('?')
        if request.method == "POST":
            dicti['hab']=request.POST['choice']
            request.session['option']=dicti
            return redirect('vote')            
        return render(request,'vote.html',{'contestantList':contestantList})
    elif post == 'tech':
        contestantList = Contestant.objects.all().filter(post='Tech').order_by('?')
        if request.method == "POST":
            dicti['tech']=request.POST['choice']
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'vote.html',{'contestantList':contestantList})
    elif post == 'cult':
        contestantList = Contestant.objects.all().filter(post='Cult').order_by('?')
        if request.method == "POST":
            dicti['cult']=request.POST['choice']
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'vote.html',{'contestantList':contestantList})
    elif post == 'welfare':
        contestantList = Contestant.objects.all().filter(post='Welfare').order_by('?')
        if request.method == "POST":
            dicti['welfare']=request.POST['choice']
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'vote.html',{'contestantList':contestantList})
    elif post == 'sports':
        contestantList = Contestant.objects.all().filter(post='Sports').order_by('?')
        if request.method == "POST":
            dicti['sports']=request.POST['choice']
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'vote.html',{'contestantList':contestantList})
    elif post == 'sail':
        contestantList = Contestant.objects.all().filter(post='SAIL').order_by('?')
        if request.method == "POST":
            dicti['sail']=request.POST['choice']
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'vote.html',{'contestantList':contestantList})
    elif post == 'swc':
        contestantList = Contestant.objects.all().filter(post='SWC').order_by('?')
        if request.method == "POST":
            dicti['swc']=request.POST['choice']
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'vote.html',{'contestantList':contestantList})
    elif post == 'bsen':
        max_len = 7
        if voter.category == '0' or voter.category == '1':
            contestantList = Contestant.objects.all().filter(post='UGS').order_by('?')
        else:
            contestantList = Contestant.objects.all().filter(post='PGS').order_by('?')
        if request.method == "POST":
            if request.POST.getlist('choice'):
                list_selected=request.POST.getlist('choice')
                for i in range(min(len(list_selected),7)):
                    key='choice'+str(i+1)
                    dicti['bsen'][key]=list_selected[i]
            else:
                dicti['bsen']['nota'] = True
            dicti['bsen']['done'] = True
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'svote.html',{'contestantList':contestantList,'max_len':max_len})
    elif post == 'gsen':
        max_len = 3
        contestantList = Contestant.objects.all().filter(post='GS').order_by('?')
        if request.method == "POST":
            if request.POST.getlist('choice'):
                list_selected=request.POST.getlist('choice')
                for i in range(min(len(list_selected),3)):
                    key='choice'+str(i+1)
                    dicti['gsen'][key]=list_selected[i]
            else:
                dicti['gsen']['nota'] = True
            dicti['gsen']['done'] = True
            request.session['option']=dicti
            return redirect('vote')
        return render(request,'svote.html',{'contestantList':contestantList,'max_len':max_len})
    
    
