from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Voter,Contestant
# from .forms import CaptchaTestForm
from functools import wraps
from datetime import datetime
import time
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from .encrypt import encryptMessage
from results.models import keys
import json as js
from django.contrib.auth.models import User

post_dictionary = {
    'vp':'VP',
    'hab':'HAB',
    'tech':'Tech',
    'cult':'Cult',
    'welfare':'Welfare',
    'sports':'Sports',
    'sail':'SAIL',
    'swc':'SWC',
    'bsen':'UGS',
    'gsen':'GS'     
}



def captcha_required(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    captcha = request.session.get('human',False)
    location = request.session.get('location',False)
    image = request.session.get('image',False)
    b = captcha and location and image
    print(captcha,location,image)
    if not b:
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
                # return HttpResponse('u have already voted')
                return render(request,'error.html',{})
            else:
                return function(request, *args, **kwargs) 
        else:
            return render(request,'error.html',{})
            # return HttpResponse('get out of here')

    return wrap

# @login_required    
# def verify(request):
#     if request.method=="POST":
#         form = CaptchaTestForm(request.POST)
#         if form.is_valid():
#             request.session['human'] = True
#             return redirect('vote')
#     else:
#         form = CaptchaTestForm()

#     return render(request, 'captchaVerify.html', {'form': form})

@login_required
@captcha_required
@is_valid
def voteCountModifier(request):
  
    dicti=request.session.get('option')
    vote_string=''
    vote_string += 'vp: '+str(dicti['vp'])+","
    
    vote_string += 'hab: '+str(dicti['hab'])+","
    
    vote_string += 'tech: ' +str(dicti['tech'])+","
    
    vote_string += 'cult: '+str(dicti['cult'])+","
    
    vote_string += 'sports: '+str(dicti['sports'])+","
       
    vote_string += 'welfare: '+str(dicti['welfare'])+","
       
    vote_string += 'sail: '+str(dicti['sail'])+","
     
    vote_string += 'swc: '+str(dicti['swc'])+","
    
    if dicti['bsen']['nota']:
        vote_string += 'bsen: NOTA,'      
    else:
        vote_string+= 'bsen: {'
        for i in range(7):
            key = 'choice'+str(i+1)
            if dicti['bsen'][key] is not None:
                vote_string += str(dicti['bsen'][key])+" "
        vote_string += '},'
    if dicti['gsen']['nota']:
        vote_string += 'gsen: NOTA,'             
    else:
        vote_string+= 'gsen: {'
        for i in range(3):
            key = 'choice'+str(i+1)
            if dicti['gsen'][key] is not None:
                vote_string += str(dicti['gsen'][key])+" "
                
        vote_string += '},'
    print(vote_string)
    return vote_string

@login_required
@captcha_required
@is_valid
def getMeSelectedCandidates(request):
    voter = Voter.objects.get(username = request.user.username)
    prog = voter.get_category_display()
    dicti=request.session.get('option')
    selectedCandidates = []
    if not dicti['vp'] == 'NOTA':
        selectedCandidates.append(('VP',Contestant.objects.get(pk=dicti['vp']),'vp'))
    else:
        selectedCandidates.append(('VP','NOTA','vp')) 
    if not dicti['hab'] == 'NOTA':
        selectedCandidates.append(('HAB',Contestant.objects.get(pk=dicti['hab']),'hab'))
    else:
        selectedCandidates.append(('HAB','NOTA','hab'))    
    if not dicti['tech'] == 'NOTA':
        selectedCandidates.append(('Technical',Contestant.objects.get(pk=dicti['tech']),'tech'))
    else:
        selectedCandidates.append(('Technical','NOTA','tech'))
    if not dicti['cult'] == 'NOTA':
        selectedCandidates.append(('Cultural',Contestant.objects.get(pk=dicti['cult']),'cult'))
    else:
        selectedCandidates.append(('Cultural','NOTA','cult'))
    if not dicti['sports'] == 'NOTA':
        selectedCandidates.append(('Sports',Contestant.objects.get(pk=dicti['sports']),'sports'))
    else:
        selectedCandidates.append(('Sports','NOTA','sports'))    
    if not dicti['welfare'] == 'NOTA':
        selectedCandidates.append(('Welfare',Contestant.objects.get(pk=dicti['welfare']),'welfare'))
    else:
        selectedCandidates.append(('Welfare','NOTA','welfare'))    
    if not dicti['sail'] == 'NOTA':
        selectedCandidates.append(('SAIL',Contestant.objects.get(pk=dicti['sail']),'sail'))
    else:
        selectedCandidates.append(('SAIL','NOTA','sail'))    
    if not dicti['swc'] == 'NOTA':
        selectedCandidates.append(('SWC',Contestant.objects.get(pk=dicti['swc']),'swc'))
    else:
        selectedCandidates.append(('SWC','NOTA','swc'))     
    
    if dicti['bsen']['nota']:
        selectedCandidates.append((prog[:2],'NOTA','bsen'))
    else:
        choice = []
        for i in range(7):
            key = 'choice'+str(i+1)
            if dicti['bsen'][key] is not None:
                choice.append((key,Contestant.objects.get(pk=dicti['bsen'][key])))
        selectedCandidates.append((prog[:2],choice,'bsen'))
    if dicti['gsen']['nota']:
        selectedCandidates.append(('GS','NOTA','gsen'))
    else:
        choice = []
        for i in range(3):
            key = 'choice'+str(i+1)
            if dicti['gsen'][key] is not None:
                choice.append((key,Contestant.objects.get(pk=dicti['gsen'][key])))
        selectedCandidates.append(('GS',choice,'gsen'))
        
    return selectedCandidates


# @login_required
# @captcha_required
# @is_valid
# def ham(request):
#     try:
#         voter = Voter.objects.get(username=request.user.username)
#     except:
#         return redirect('vote')
#         

@login_required
@captcha_required
@is_valid
def vote_for(request,post):
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
    posts_done = request.session.get('posts_done',
        {
            'VP': '-1',
            'HAB': '-1',
            'Tech':'-1',
            'Cult':'-1',
            'Welfare':'-1',
            'Sports':'-1',
            'SAIL':'-1',
            'SWC':'-1',
            'UGS': '-1',
            'PGS':'-1',
            'Girls':'-1',

        }
    )
    if not posts_done[post_dictionary[post]].startswith("Current"):
        posts_done[post_dictionary[post]] = "Current " + str(posts_done[post_dictionary[post]])
    contestantList = Contestant.objects.all().filter(post=post_dictionary[post]).order_by('?')
    pks = []
    for i in contestantList:
        pks.append(i.pk)
    if request.method == "POST":
        try:
            choice = request.POST['choice']
        except:
            return redirect('vote')
        
        if request.POST['choice'] == post_dictionary[post]:
            dicti[post] = 'NOTA'
            posts_done[post_dictionary[post]] = "NOTA"
        else:
            try:
                cont = Contestant.objects.get(pk=request.POST['choice'])
            except:
                return redirect('vote')
            if cont.post == post_dictionary[post]:
                dicti[post]=request.POST['choice']
                posts_done[post_dictionary[post]] = str(dicti[post])
        request.session['option']=dicti
        request.session['posts_done']=posts_done
        return redirect('vote')
    print(posts_done)
    return render(request,'vote.html',{'contestantList':contestantList,'pks':pks,'post':contestantList[0].get_post_display(),'ham':[(k, v) for k, v in posts_done.items()],'selected':posts_done[post_dictionary[post]]})


@login_required
@captcha_required
@is_valid
def vote(request):
    # global key = []
    key =[]
    try:
        # print(users[0])
        key.append(keys.objects.get(user= User.objects.get(username='swc@iitg.ac.in')))
        key.append(keys.objects.get(user=User.objects.get(username='alan@iitg.ac.in')))
        key.append(keys.objects.get(user=User.objects.get(username='saketkumar@iitg.ac.in')))
        request.session['ready'] = True
    except:
        # print(users[0])
        request.session['ready'] = False
        print("damn")
        return redirect('captcha')
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
    if voter.category == '0' or voter.category == '2':
        request.session['total_no'] = 9
    else:
        request.session['total_no'] = 10
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
    posts_done = request.session.get('posts_done',
        {
            'VP': '-1',
            'HAB': '-1',
            'Tech':'-1',
            'Cult':'-1',
            'Welfare':'-1',
            'Sports':'-1',
            'SAIL':'-1',
            'SWC':'-1',
            'UGS': '-1',
            'PGS':'-1',
            'Girls':'-1',

        }
    )
    if voter.category == '0':
        posts_done['Girls'] = '-2'
        posts_done['PGS'] = '-2'
    elif voter.category == '1':
        posts_done['PGS'] = '-2'
    elif voter.category == '2':
        posts_done['Girls'] = '-2'
        posts_done['UGS'] = '-2'
    else:
        posts_done['UGS'] = '-2'

    request.session['posts_done'] = posts_done
        
    if post is None:
        selectedCandidates = getMeSelectedCandidates(request)
        if request.method == "POST":
            try:
                choice = request.POST['choice']
            except:
                return redirect('vote')
            
            if request.POST['choice'] == "done":
                voter.final_submit = True
                vote_string=voteCountModifier(request)  
                #encrypt the string using our function
                # 103 and 147
                # vote_string = js.dumps(request.session['option'])
                # print(vote_string)    
                voter.vote_time = time.time()
                voter.vote_string1 = encryptMessage(key,
                    vote_string[:100], int(voter.vote_time))
                voter.vote_string2 = encryptMessage(key,
                    vote_string[100:], int(voter.vote_time))
                voter.voter_location = Point(request.session['longitude'], request.session['latitude'])
                voter.save()
                return render(request,'thankyou.html',{})
            elif request.POST['choice'] == "bsen" or request.POST['choice'] == "gsen":
                dicti[request.POST['choice']]['done']=False
                dicti[request.POST['choice']]['nota']=False
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
    
    elif not (post == 'bsen' or post == 'gsen'):
        return vote_for(request,post)
    
    elif post == 'bsen':
        if not posts_done[post_dictionary[post]].startswith("Current"):
            posts_done[post_dictionary[post]] = "Current "+posts_done[post_dictionary[post]]
        max_len = 7
        cont_post = 'UGS'
        if voter.category == '0' or voter.category == '1':
            contestantList = Contestant.objects.all().filter(post='UGS').order_by('?')
        else:
            post_dictionary['bsen'] = 'PGS'
            contestantList = Contestant.objects.all().filter(post='PGS').order_by('?')
            cont_post = 'PGS'
        pks = []
        for i in contestantList:
            pks.append(i.pk)
        if request.method == "POST":
            if request.POST.getlist('nota'):
                dicti['bsen']['nota'] = True
                posts_done[post_dictionary[post]] = "NOTA"
            elif request.POST.getlist('choice'):
                list_selected=request.POST.getlist('choice')
                listToStr = ' '.join([str(elem) for elem in list_selected]) 
                posts_done[post_dictionary[post]] = listToStr
                for i in range(min(len(list_selected),7)):
                    try:
                        cont = Contestant.objects.get(pk=list_selected[i])
                    except:
                        return redirect('vote')
                    if not cont.post == cont_post:
                        return redirect('vote')
                    key='choice'+str(i+1)
                    dicti['bsen'][key]=list_selected[i]
            else:
                return redirect('vote')
            dicti['bsen']['done'] = True
            request.session['option']=dicti
            request.session['posts_done']=posts_done
            return redirect('vote')
        print(posts_done)
        return render(request,'svote.html',{'contestantList':contestantList,'pks':pks,'max_len':max_len,'post':contestantList[0].get_post_display(),'ham':[(k, v) for k, v in posts_done.items()],'selected':posts_done[post_dictionary[post]]})
    elif post == 'gsen':
        if not posts_done['Girls'].startswith("Current"):
            posts_done['Girls'] = "Current "+posts_done['Girls']
        max_len = 3
        contestantList = Contestant.objects.all().filter(post='GS').order_by('?')
        pks = []
        for i in contestantList:
            pks.append(i.pk)
        if request.method == "POST":
            if request.POST.getlist('nota'):
                posts_done['Girls'] = "NOTA"
                dicti['gsen']['nota'] = True
            elif request.POST.getlist('choice'):
                list_selected=request.POST.getlist('choice')
                listToStr = ' '.join([str(elem) for elem in list_selected]) 
                posts_done['Girls'] = listToStr
                for i in range(min(len(list_selected),3)):
                    try:
                        cont = Contestant.objects.get(pk=list_selected[i])
                    except:
                        return redirect('vote')
                    if not cont.post == 'GS':
                        return redirect('vote')
                    key='choice'+str(i+1)
                    dicti['gsen'][key]=list_selected[i]
            else:
                return redirect('vote')
            dicti['gsen']['done'] = True
            request.session['option']=dicti
            request.session['posts_done']=posts_done
            return redirect('vote')
        print(posts_done)
        return render(request,'svote.html',{'contestantList':contestantList,'pks':pks,'max_len':max_len,'post':contestantList[0].get_post_display(),'ham':[(k, v) for k, v in posts_done.items()],'selected':posts_done['Girls']})
