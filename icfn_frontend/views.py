from django.shortcuts import render
from faq.models import *
from captcha.fields import CaptchaField, CaptchaTextInput
from django.shortcuts import get_object_or_404
from icfn_new.settings import HOST_URL,PHOTO_URL,SENDER_MAIL,RECEIVER_MAIL,ADMIN_SENDER_MAIL , ICFN_INFO_MAIL
from rest_framework.response import Response
from faq.views import send_sandgridmail
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from uuid import uuid4
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from NGO.models import *
from mcms.models import *
import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
import json
from .templatetags.frontend_templatetags import get_ftype_fundraisers
from django.utils.html import strip_tags
from django.template import RequestContext
from django.shortcuts import render
from .common_function import frontend_pagination
from django.utils.encoding import smart_text
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.views import View
from math import ceil
from django.views.decorators.csrf import csrf_exempt

from django.core.files.uploadedfile import SimpleUploadedFile

import _datetime
today = _datetime.date.today()

from datetime import *
# date = datetime.datetime.now()
# date.strftime('%Y-%m-%d')


curr_yr = datetime.today().year
tod = datetime.today()
sdy = '01'
smn = '04'
curr_month = datetime.today().month
if curr_month > 3:
    syr = datetime.today().year
else:
    syr = datetime.today().year - 1
edy = '31'
emn = '03'
eyr = syr+1
s = str(syr)+'-'+smn+'-'+sdy
e = str(eyr)+'-'+emn+'-'+edy
ssd = datetime.strptime(s,'%Y-%m-%d').date()
eed = datetime.strptime(e,'%Y-%m-%d').date()


def userid():
    return uuid4().hex

def index(request): 
    featured = Event.objects.filter(active=True,feature_event=True).order_by('-id')[0:2]
    ################## Homepage Accross the country ############
    # Homepage accross the country, and Speach section are added independantly
    # its not depends on any event
    # in accross the country section title and description and banner and video
    # in home page speach section headline title videos and byline is added
    ####################################################
    accross_obj = AccrossTheCountry.objects.filter(active=True).latest('id')
    if accross_obj.banner:
        banner = PHOTO_URL+"static"+accross_obj.banner.url 
    else:
        banner = ''
    homepage_speach_obj = HomePageSpeak.objects.filter(active=True).latest('id')
    home_banner = HomeBanner.objects.filter(active = True)
    home_banner_list = []
    for obj in home_banner:
        home_banner_list.append({"id":obj.id,"image":PHOTO_URL+obj.image.url})
    
###################### Associated List #####################################
    associated_list= []
    # featured_event_lst = Event.objects.filter(active=True,end_date__gte=datetime.today(),event_type='Marathon').order_by('?')#,active=True, end_date__gte=datetime.today()
    featured_event_lst1 = Event.objects.filter(active=True,event_type='Marathon').order_by('?')#,active=True, end_date__gte=datetime.today()
    featured_event1 = featured_event_lst1[0]
    csr_list = [{"caption":"Company","csrname":i.name} for i in DuplicateCorporates.objects.filter(created_on__range=(ssd, eed),active=True,event=featured_event1).order_by('?')[:10]]

    ngo_objs = featured_event1.ngo.filter(created_on__range=(ssd, eed),register_status=2,active=True).order_by('?')
    [associated_list.append({'caption':'CSO','image': PHOTO_URL +cso.icon.url if cso.icon else '','text':cso.name,'key':"ngo"}) for cso in ngo_objs.order_by('-id')[:10]]
    associated_list = associated_list + csr_list
    print(featured_event_lst1)

############################# for the Be a champion #Because you care section ###############################
    # import ipdb;ipdb.set_trace()
    featured_event_lst = Event.objects.filter(active=True,feature_event=True,event_type='Marathon').order_by('-id')#,active=True, end_date__gte=datetime.today()
    if featured_event_lst:
        featured_event = featured_event_lst[0]
        if featured_event.join_us_logo:
            champion_logo = featured_event.join_us_logo.url
        # ngo_obj = NGO.objects.filter(event=featured_event,register_status=2,active=True).order_by('?')
        ngo_obj = featured_event.ngo.filter(event=featured_event,register_status=2,active=True).order_by('?')[:3]
    else:
        featured_event = 0
        ngo_obj = []

    for i in ngo_obj:
        if i.icon:
            image = PHOTO_URL +"static"+i.icon.url
        else:
            image = ''
    # champion_logo = PHOTO_URL +"static"+ champion_logo
    return render(request, 'frontend_templates/index.html', locals())

def frontendlogin(request):     
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # import ipdb;ipdb.set_trace()
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                msg = "User is not active"
            elif user is not None:
                login(request, user)
                login_successfull = "User Logged in Successfully"
                try:
                    user_id = UserProfile.objects.filter(user_id=user.id).latest('id').id
                    ngo_id = NGO.objects.get(contact_person_id=user_id).id
                    request.session["ngo_id"]=ngo_id
                except:
                    pass
                return HttpResponseRedirect('/cso-registration/')
        else:
            # invalid login
            msg = 'Please enter a valid username and password'

    return render(request,'frontend_templates/login.html',locals())  

def state_data(request, pk):
    if request.method == 'POST':
        state_list = State.objects.filter(country_id = pk).values('id','name').order_by('name')
    return JsonResponse({'state_list': list(state_list)})   

def UserActivation(activation_key):
    # function UserActivation
    # this function is used to activate the user
    # activation_key specifies the key for the user
    # based on the key activation object will be retrived
    # if activation object is found
    # user object will be retrived
    # user.is_active=True activates the user
    # user.save() save the user object
    # useractobj.is_active=True activates the individual activate object
    # useractobj.save() save the individual activation object
    # if user is already activated
    # it will display an error message
    # if any changes in the activation key throws error as key mismathed
    user = 0
    try:
        useractobj = IndividualActivation.objects.get(activation_key=activation_key)
        if not useractobj.is_active:
            user = User.objects.get(username=useractobj.user.username)
            user.is_active=True
            user.save()
            useractobj.is_active=True
            useractobj.save()
            msg = "your account is activated"
            return Response({"status":2,"message":msg,"user_id":user.id})

        else:
            msg = "Your account is already activated"
            user = User.objects.get(username=useractobj.user.username)
            return Response({"status":2,"message":msg,"user_id":user.id})

    except:
        return Response({"status":0,"message":"Key Mismatched"})




def signup(request):
    # import ipdb;ipdb.set_trace()

    countries=Country.objects.all()
    states=State.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        country_data = request.POST.get('country')
        state_data = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        signup_form = request.POST.get('signup_form')

        country = request.POST.get('country')
        state = request.POST.get('state')


        # countryobj = ''
        # countryobj, created = Country.objects.get_or_create(name=country)
        countryobj, created = Country.objects.get_or_create(name=country)
        stateobj, created = State.objects.get_or_create(name=state,country=countryobj)
        
        
        # stateobj, created = State.objects.get_or_create(name=state,country=countryobj)

        if User.objects.filter(username=email).exists():
            msg ={"message":"User Already Exists"}

            #return Response({"status":0,"message":msg})
            return render(request,'frontend_templates/signup.html',locals())

        if signup_form == 'Personal':
            user_obj = User.objects.create_user(username=email,email=email,password=password1)
            user_obj.last_name = lname if lname else ''
            user_obj.first_name = fname
            user_obj.is_active = False
            user_obj.save()
            UserDetails.objects.create(user=user_obj, username=email, password=password1)      

            user_profile_obj = UserProfile.objects.create(user=user_obj,usertype='2',title_id=title)
            Address.objects.create(address1=address1,address2=address2,
                 pincode=pincode,country_id=countryobj.id,state_id=stateobj.id,mobile=mobile,
                 content_type=ContentType.objects.get(model__iexact='user'),object_id = user_obj.id,city=city)
            activation_key = userid()
            individual_activate = IndividualActivation(user=user_obj,activation_key=activation_key)
            individual_activate.save()
            actlink = UserActivation(str(activation_key))
            #print(actlink)
            sub = "User Registered Successfully on India Cares Website"
            content = render_to_string('Archive/index.html',{'today': datetime.datetime.today(), 'user_obj': user_obj,'title':user_profile_obj.title,'password':password1, 'actlink':actlink})
            #print(content)
            sender_mail = ADMIN_SENDER_MAIL #SENDER_MAIL
            DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(user_obj), object_id=user_obj.id,html="user_registration.html", mailtype="Registration", 
                text="User registration", sender=ADMIN_SENDER_MAIL, receiver=[user_obj.email,], functionname="add_individual_register()")
            smail = send_sandgridmail(sender=sender_mail,
                #receiver=[(user_obj.email,"")],
                receiver=[ADMIN_SENDER_MAIL,],
                subject=sub,content=content,reply_to=sender_mail)
            subject = "Account Details for "+ user_obj.first_name + " at India Cares Foundation"
            message = "Hello Administrator," +"<br>"+ "A new user has registered at icfn.in."+ "<br>" +"This e-mail contains their details:"+"<br>"+"Name: "+user_obj.first_name+"\n"+"E-mail: "+user_obj.email+"<br>"+"Please do not respond to this message. It is automatically generated and is for information purposes only."
 #                """receiver_mail = [ADMIN_SENDER_MAIL,]"""

            receiver_mail = [(RECEIVER_MAIL,"")]
            DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(user_obj), object_id=user_obj.id,html="user_registration.html", mailtype="AdminMails", text="Admin mail for user registration", sender=ADMIN_SENDER_MAIL, receiver=[RECEIVER_MAIL,], functionname="IndividualRegister()")
            send_sandgridmail(sender=sender_mail,receiver=receiver_mail,subject=subject,content=message)
            msg = {"status":2,"message":"Thank You for Registering to Make a Difference. Please Activate Your Account Through the Mail You Have Received"}
        else:
            msg = {"status":0,"message":'Form Is Invalid'}

    return render(request,'frontend_templates/signup.html',locals())  


def get_divide_corporate_team(obj_string):
    return "corporate" in obj_string.lower()

# Function to get the Count for each Fundraiser Type
def get_duplicatecorp(event_obj):
    participate_list = []
    [participate_list.append({'count':get_ftype_fundraisers(event_obj.id,item.id) or event_obj.fundraisers.filter(fundraiser_type=item.id, active=True,
    created_by__is_active=True).count(),"id":item.id,"url":"/fundraiser-type",'name':str(item.name),"corp":get_divide_corporate_team(item.name)})for item in event_obj.allowed_categories.all().order_by('event_index')]
    return participate_list

""" Functional View for Event Detail Page"""
def get_champion_corporate_list(event_obj,search=None):
# champion listing    
    champion_list ,corporate_list = [],[]
    if search:
        for event in event_obj.display.filter(active=True):
            for champion in event_obj.fundraisers.filter(fundraiser_type = event, active=True, created_by__is_active=True,display_name__icontains=search).order_by('?'):
                words = strip_tags(champion.description)[:95] + '...'
                champion_list.append({'color':event_obj.color,'image':champion.icon.url if champion.icon else PHOTO_URL +"/static/frontend/img/no-image.jpg",
                                    'header':"Champion for "+"- "+champion.ngo.name,
                                    'name':champion.display_name,
                                    'id':champion.id,
                                    "accept_donation":event_obj.accept_donation,
                                    'title_slug':champion.display_name.replace(' ','_') if champion.display_name else '',
                                    'description':words,"slug":champion.slug,'key':"fundraiser","ngo_name":champion.ngo.name})
    # corporates listing
        for corporates in DuplicateCorporates.objects.filter(active=True, event=event_obj,name__icontains=search).order_by('?'):
            for ngo in corporates.many_ngos.all():
                corporate_list.append({'color':event_obj.color,'text':ngo.name,'name':corporates.name,"slug":ngo.slug})
                
    else:
        for event in event_obj.display.filter(active=True):
            for champion in event_obj.fundraisers.filter(fundraiser_type = event, active=True, created_by__is_active=True).order_by('?'):
                words = strip_tags(champion.description)[:95] + '...'
                champion_list.append({'color':event_obj.color,'image':champion.icon.url if champion.icon else PHOTO_URL +"/static/frontend/img/no-image.jpg",
                                    'header':"Champion for "+"- "+champion.ngo.name,
                                    'name':champion.display_name,
                                    'id':champion.id,
                                    "accept_donation":event_obj.accept_donation,
                                    'title_slug':champion.display_name.replace(' ','_') if champion.display_name else '',
                                    'description':words,"slug":champion.slug,'key':"fundraiser","ngo_name":champion.ngo.name})
    # corporates listingeventdetail
        for corporates in DuplicateCorporates.objects.filter(active=True, event=event_obj).order_by('?'):
            for ngo in corporates.many_ngos.all():
                corporate_list.append({'color':event_obj.color,'text':ngo.name,'name':corporates.name,"slug":ngo.slug})
               
    if  champion_list:
        champion_list=[champion_list[-1]]
    if corporate_list:
        corporate_list=[corporate_list[-1]]
    return champion_list,corporate_list

def eventdetail(request,event_slug):
    event = Event.objects.get(active=True, slug=event_slug)
    total_participating_csos = event.ngo.filter(active=True).count() # Total Active CSO Participating in the event
    allowed_categories = get_duplicatecorp(event)
    cso = event.ngo.filter(active=True).order_by('?')[0:1] # listing of cso
    champion_list = get_champion_corporate_list(event)[0]
    corporate_list = get_champion_corporate_list(event)[1]
    links = Link.objects.filter(content_type__model__iexact="event",object_id=event.id).order_by('-id') #last year hightlight data 
    return render(request,'frontend_templates/event_detail.html',locals())  


## for getting the all participating cso in event
def cso_listing(request,event_slug):
    cso_name = request.GET.get("cso_name")
    cause = request.GET.get("cause")
    event = Event.objects.get(active=True, slug=event_slug)
    total_participating_csos = event.ngo.filter(active=True).count() #count of cso 
    cso = event.ngo.filter(active=True).order_by('name')
    ngo_cause_ids = NGO.objects.filter(active=True).values_list('cause__id',flat=True)
    select_cause = Cause.objects.filter(active=True,id__in=ngo_cause_ids).order_by('name')
    if cso_name:
        cso = cso.filter(name__icontains=cso_name)
    if cause:
        cso = cso.filter(cause__id=int(cause))
    obj_list = frontend_pagination(request,cso)
    return render(request, 'frontend_templates/cso_listing.html', locals())


## fundraiser listing in event 
def fundraisers_listing(request,event_slug):
    fundraiser_name = request.GET.get("fundraiser_name")
    cause = int(request.GET.get("cause",0))
    event = Event.objects.get(active=True, slug=event_slug) #event slug
    champion_list = get_champion_corporate_list(event)[0] 
    total_participating_fundraiser = event.fundraisers.filter(active=True).count() #count of fundraisers
    fundraiser_list = Fundraiser.objects.filter(active=True,event=event,created_by__is_active=True) #all participating fundraisers details in event details page 
    cso = event.ngo.filter(active=True).order_by('name')
    ngo_cause_ids = NGO.objects.filter(active=True).values_list('cause__id',flat=True)
    select_cause = Cause.objects.filter(active=True,id__in=ngo_cause_ids).order_by('name')
    if fundraiser_name:
        fund_name = fundraiser_name.strip()
        name = fund_name.split(" ")
        if len(fund_name) >= 1:
            if len(name) == 1:
                fundraiser_list = fundraiser_list.filter(Q(created_by__first_name__istartswith=fund_name)
                                                        | Q(created_by__last_name__istartswith=fund_name)
                                                        |Q(display_name__icontains=fund_name)
                                                        )	
            else:
                fundraiser_list = fundraiser_list.filter(Q(created_by__first_name__istartswith=name[0])
                                                        | Q(created_by__last_name__istartswith=name[1])
                                                        |Q(display_name__icontains=fund_name)
                                                        )
        # fundraiser_list = fundraiser_list.filter(name__icontains=name)
    if cause:
        fundraiser_list = fundraiser_list.filter(ngo__cause__id=int(cause))
    obj_list = frontend_pagination(request,fundraiser_list)					
    return render(request, 'frontend_templates/fundraisers_listing.html',locals())


def get_event_donation_amount(event_obj):
    amt=0
    offamt = 0
    d = Donation.objects.filter(payment_status='Success', event=event_obj).filter(event__active=True)
    d1 = OfflineDonation.objects.filter(event=event_obj).filter(event__active=True)
    for i in d:
        amt = amt + i.amount
    for offd in d1:
        offamt = offamt + offd.amount
    tot_amt = amt + offamt
    return int(tot_amt)


def link_obj(obj):
	data = {}
	if obj.image:
		data = {"image":PHOTO_URL+obj.image.url,"caption":"image","title":obj.name}
		return data
	else:
		data = {"url":obj.URL,"caption":"video","title":obj.name}
		return data
	return None

def campaigndetail(request, event_slug):
    event = Event.objects.get(active=True, slug=event_slug,event_type='Campaign')
    fundraiser_button = False
    view_fundraiser = False
    view_cso = False
    if event.campaign_type == "GC":#General Capaign
        fundraiser_button = False
        view_fundraiser = False
        view_cso = False
    elif event.campaign_type == "CFC":#Campaign with CSO AND fundraiser
        fundraiser_button = True
        view_fundraiser = True
        view_cso = True
    elif event.campaign_type == "FC":
        fundraiser_button = True
        view_fundraiser = True
        view_cso = False
    banner_image = PHOTO_URL+ "static" + event.banner_image.url if event.banner_image else ""
    logo = PHOTO_URL + "static" + event.widget_icon.url if event.widget_icon else ""
    description = EventExtended.objects.get_or_none(event=event).our_work[:300] if EventExtended.objects.get_or_none(event=event) else ""
    description_second = EventExtended.objects.get_or_none(event=event).support_for_the_cause if EventExtended.objects.get_or_none(event=event) else ""
    full_description = EventExtended.objects.get_or_none(event=event).our_work  if EventExtended.objects.get_or_none(event=event) else "",
    target = int(event.target) if event.target else ""
    donated_amount = get_event_donation_amount(event) if get_event_donation_amount(event) else 0
    perentage_collection = (donated_amount/target)*100
    our_mission = EventExtended.objects.get_or_none(event=event).mission if EventExtended.objects.get_or_none(event=event) else ""

    """
	campaign gallary is showing here images and
	videos are querying from link table 
	its generic type 
	"""
    gallary_obj = Link.objects.filter(active=True,content_type=ContentType.objects.get(model__iexact='event'),object_id=event.id)
    slides = [link_obj(obj) for obj in gallary_obj if link_obj(obj) != None]
    return render(request,'frontend_templates/campaign_detail.html',locals()) 

#----------------------------------------------------------------------------------------------
def event_aboutus(request, event_slug):
    event = Event.objects.get(active=True, slug=event_slug)     
    return render(request,'frontend_templates/event_aboutus_page.html',locals())  

def event_faq(request, event_slug):
    event = Event.objects.get(active=True, slug=event_slug) 
    faq_cat = FaqCategory.objects.filter(event__slug__icontains=event_slug[:3], is_active=True)
    return render(request,'frontend_templates/event_faq.html',locals())  

def event_gallery(request, event_slug): 
    event = Event.objects.get(active=True, slug=event_slug) 
    # gallery videos
    links = Link.objects.filter(content_type__model__iexact="event",object_id=event.id)
    return render(request,'frontend_templates/event_gallery.html',locals())

############## event annual report function ###############################
def annual_report(request): 
    reportlist = AnnualReport.objects.filter(active=True,filetype='Annual Report').order_by('-id')
    return render(request,'frontend_templates/annual_reports.html',locals())


############## event dockets function ###############################
def dockets(request):
    reportlist = AnnualReport.objects.filter(active=True,filetype='Docket').order_by('-event__name','event__id','-name','-id')
    return render(request, 'frontend_templates/dockets.html',locals())
 # [report_list.append({"pdf":PHOTO_URL + '/'+str(report.attach_file) 
#  if report.attach_file else report.url ,'image':PHOTO_URL +report.image.url
#  if report.image else PHOTO_URL +"/static/frontend/img/no-image.jpg",
# 'upload_description':report.name})for report in reportlist]



def fundraiser_overview(request, event_slug):
    event = Event.objects.get(active=True, slug=event_slug)
    event_article = EventArticle.objects.get_or_none(slug=event_slug, content_type__model='event', object_id=event.id)
    cat_list = event.allowed_categories.all()
    f_cat = FundraiserType.objects.filter(active=True, id__in=cat_list)
    faq_cat = FaqCategory.objects.filter(name="Fundraisers")
    event_video = Link.latest_link(content_type__model__iexact="event", object_id=event.id) 
    return render(request,'frontend_templates/fundraiser_overview.html',locals())


         
def get_cso_related_i_champions(ngo,event_obj):
    # cmapion list contains gold
    # silver, platinum, diamond 
    # listing
    # cso_list icare listing
    champion_list, cso_list , corp_lis = [],[],[]

    # for champion in Fundraiser.objects.filter(ngo=ngo, active=True,created_by__is_active=True,
                                                # fundraiser_type_id__in=[4,8,16,24],created_on__gte=event_obj.created_on).order_by('?'):
    for champion in event_obj.fundraisers.filter(ngo=ngo, active=True,created_by__is_active=True,
                                                fundraiser_type_id__in=[4,8,16,24,40,41]).order_by('?'):
        cso_list.append({'image':str( PHOTO_URL +champion.icon.url) if champion.icon else PHOTO_URL +"/static/frontend/img/no-image.jpg",
                                'header':champion.fundraiser_type.name,"accept_donation":event_obj.accept_donation,
                                'name':champion.display_name or champion.created_by.first_name ,'id':champion.id,
                                "slug":champion.slug,'key':"fundraiser","share_description":champion.ngo.our_mission})   
    # for champion in Fundraiser.objects.filter(ngo=ngo, active=True,created_by__is_active=True,
    #                                             fundraiser_type_id__in=[9,10,13,14,17],created_on__gte=event_obj.created_on).order_by('?'):
    for champion in event_obj.fundraisers.filter(ngo=ngo, active=True,created_by__is_active=True,
                                                fundraiser_type_id__in=[10,21,37,38,9,22,17,13,20,36,14]).order_by('?'):
        champion_list.append({'image':str( PHOTO_URL +champion.icon.url) if champion.icon else PHOTO_URL +"/static/frontend/img/no-image.jpg",
                                'header':champion.fundraiser_type.name,"accept_donation":event_obj.accept_donation,
                                'name':champion.display_name,'id':champion.id,
                                "slug":champion.slug,'key':"fundraiser","share_description":ngo.our_mission})
    for corp in DuplicateCorporates.objects.filter(active=True,many_ngos=ngo,event=event_obj):
        corp_lis.append({"slug":ngo.slug,"text":corp.name,"name":ngo.name,
                        "no_team":corp.no_of_teams,"team":corp.team})
    return cso_list,champion_list,len(cso_list),len(champion_list),corp_lis

def get_ngo_taxstatus(cso_obj):
    tax = []
    [tax.append("12A") if cso_obj.a12 == 'VA' or cso_obj.a12 == 'PM' else ""]
    [tax.append("80G") if cso_obj.validity_80G == 'VA' or cso_obj.validity_80G == 'PM'else ""]
    [tax.append("35AC") if cso_obj.validity_35AC == 'VA' else ""]
    [tax.append("FCRA") if cso_obj.fcra == 'VA' else ""]
    return ','.join(tax)


def event_ngo_obj_data(cso,e_cso,attr):
    data_val = ''
    # if e_cso:
    if attr == 'phone1':
        try:
            if e_cso.phone1:
                data_val = e_cso.phone1
            else:
                data_val = cso.phone1
        except:
            data_val = cso.phone1
    elif attr == 'mobile':
        try:
            if e_cso.mobile:data_val = e_cso.mobile
            else:data_val = cso.mobile
            # data_val = e_cso.mobile
        except:
            data_val = cso.mobile
    elif attr == 'web_address':
        try:
            if e_cso.web_address:data_val = e_cso.web_address
            else:data_val = cso.web_address
        except:
            data_val = cso.web_address
    elif attr == 'fund_utilization':
        try:
            if e_cso.fund_utilisation_statement:data_val = e_cso.fund_utilisation_statement
            else:data_val = cso.fund_utilisation_statement
        except:
            data_val = cso.fund_utilisation_statement
    elif attr == 'city':
        try:
            if e_cso.city:data_val = e_cso.city
            else:data_val = cso.city
        except:
            data_val = cso.city
    elif attr == 'black_board_message':
        try:
            if e_cso.black_board_message:data_val = e_cso.black_board_message
            else:data_val = cso.black_board_message
        except:
            data_val = cso.black_board_message
    elif attr == 'our_mission':
        try:
            if e_cso.our_mission:data_val=e_cso.our_mission
            else:data_val = cso.our_mission
        except:
            data_val = cso.our_mission

    elif attr == 'address':
        # import ipdb;ipdb.set_trace()
        try:
            if e_cso.address1:
                data_val = smart_text(smart_text(e_cso.address1) + " "+ smart_text(e_cso.address2) + " "+ smart_text(e_cso.city) + " "+smart_text(e_cso.state) +" "+ smart_text(e_cso.country) + " "+ smart_text(e_cso.pincode)) 
            else:
                data_val=smart_text(smart_text(cso.address1) + " " +smart_text(cso.address2) + " "+ smart_text(cso.city) + " "+ smart_text(cso.state) +" "+ smart_text(cso.country) +"-"+ smart_text(cso.pincode))
        except:
            data_val=smart_text(smart_text(cso.address1 if cso.address1 else " ") + " " +smart_text(cso.address2 if cso.address2 else " ") + " "+ smart_text(cso.city if cso.city else " ") + " "+ smart_text(cso.state if cso.state else " ") +" "+ smart_text(cso.country if cso.country else " ") +" "+ smart_text(cso.pincode if cso.pincode else " "))
    elif attr == 'work_acheivement':
        try:
            if e_cso.work_acheivement:data_val = e_cso.work_acheivement
            else:data_val=cso.work_acheivement         
        except:
            data_val=cso.work_acheivement
    if not data_val:
        data_val = ""
    return data_val

#Function to Get the Total Donated Amount for the particular ngo
def donation_total_amount(ngo_id,event_id):
    ngo = NGO.objects.get(id=ngo_id)
    amt=0
    offamt = 0
    # d = Donation.objects.filter(created_on__range=(ssd, eed),ngo_id=ngo_id, payment_status='Success',event_id=event_id).filter(event__active=True)
    d = Donation.objects.filter(ngo_id=ngo_id, payment_status='Success',event_id=event_id).filter(event__active=True)
    f_ids = Fundraiser.objects.filter(event=event_id,ngo=ngo).values_list('id',flat=True)
    # d1 = OfflineDonation.objects.filter(created_on__range=(ssd, eed),active=True,fundraiser_id__in=f_ids,event_id=event_id).filter(event__active=True)
    d1 = OfflineDonation.objects.filter(active=True,fundraiser_id__in=f_ids,event_id=event_id).filter(event__active=True)
    for i in d: 
        amt = amt + i.amount
    for offd in d1:
        offamt = offamt + offd.amount
    tot_amt = amt + offamt
    return tot_amt

#Do Not Change the Existing Variables in the Code
def cso_details(request, event_slug, cso_slug):
    event = Event.objects.get(active=True, slug=event_slug)
    today = _datetime.date.today()
    msg = "Page Not Found Please Contact Administrator."
    fundraiser_list = Fundraiser.objects.filter(active=True,event=event,created_by__is_active=True)
    cso_obj = event.ngo.get(active=True,slug=cso_slug)
    sub_listing = get_cso_related_i_champions(cso_obj,event)
    cso_list = sub_listing[0]
    champion_list = sub_listing[1]
    corp_lis = sub_listing[4]

    # champion_list = get_cso_related_i_champions(cso_obj,event)
    # cso_list = get_cso_related_i_champions(cso_obj,event)
    # corp_lis = get_cso_related_i_champions(cso_obj,event)
    cso_len = len(cso_list)
    cham_len= len(champion_list)
    # ngo_description = EventNgoDescription.objects.filter(event=event, ngo_id=cso_obj.id,active=True).latest('id')
    address = Address.objects.get(content_type=ContentType.objects.get(model__iexact='ngo'), object_id=cso_obj.id)
    try:
        ngo_description = EventNgoDescription.objects.filter(event=event, ngo_id=cso_obj.id,active=True).latest('id')
    except:
        ngo_description = None
        pass 
    tax = get_ngo_taxstatus(cso_obj)
    contact1 = NgoCommunication.objects.get(ngo=cso_obj)
    contact_person_name =  str( str(cso_obj.contact_person.title) +" "+ str(cso_obj.contact_person.user.first_name) +" "+ str(cso_obj.contact_person.user.last_name))
    contact = ngo_description.contact_person if ngo_description else contact_person_name
    if ngo_description:
        if ngo_description.contact_person:
            contact_person_name = ngo_description.contact_person
        else:
            contact_person_name = contact_person_name
    else:
        contact_person_name = contact_person_name
    phone = event_ngo_obj_data(contact1,ngo_description,'phone1') or contact1.phone2
    address1 = event_ngo_obj_data(address, ngo_description, "address")
    web = event_ngo_obj_data(contact1,ngo_description,'web_address')
    cso_email = ngo_description.email if ngo_description else cso_obj.contact_person.user.email
    mobile = event_ngo_obj_data(contact1,ngo_description,'mobile') or address.mobile
    black_board_message = event_ngo_obj_data(cso_obj,ngo_description,'black_board_message')
    our_mission = event_ngo_obj_data(cso_obj,ngo_description,'our_mission')
    if cso_obj.youtube_embedd:
        video = cso_obj.youtube_embedd
    else:
        for vid_obj in event.get_videos_for_event()[:1]:
            video  = vid_obj.URL
    total_amount = cso_obj.goal_amount if cso_obj.goal_amount else 0
    try:
        donated_amount = int(donation_total_amount(cso_obj.id, event.id)) 
    except:
        donated_amount = 0
    try:
        perentage_collection = (donated_amount/total_amount)*100
    except:
        perentage_collection = 0
    Our_mission_description = event_ngo_obj_data(cso_obj,ngo_description,'work_acheivement')[:250] + '...' if len(strip_tags(event_ngo_obj_data(cso_obj,ngo_description,'work_acheivement'))) > 250 else ''
    Ngo_full_description = event_ngo_obj_data(cso_obj,ngo_description,'work_acheivement')
    return render(request,'frontend_templates/cso_details.html', locals())

    # this function decides the badge of the champion
def get_badge_icon(f_obj):
    champion_gold = ""
    if 'Diamond' in f_obj.fundraiser_type.name:
        champion_gold =  PHOTO_URL +"static/images/icon/diamond.png"
    elif 'Gold' in f_obj.fundraiser_type.name:
        champion_gold = PHOTO_URL + "static/images/icon/champion_gold.png"
    elif 'Platinum' in f_obj.fundraiser_type.name:
        champion_gold = PHOTO_URL + "static/images/icon/platinum.png"
    elif 'Silver' in f_obj.fundraiser_type.name:
        champion_gold =  PHOTO_URL +"static/images/icon/silver.png"
    else:
        champion_gold =  PHOTO_URL +"static/images/icare_badge.png"
    return champion_gold



def fundraisers_details(request, event_slug, fund_slug):
    event = Event.objects.get(active=True, slug=event_slug)
    today = _datetime.date.today()
    msg = "Page Not Found Please Contact Administrator."
    fundraiser_list = Fundraiser.objects.filter(active=True,event=event,created_by__is_active=True)
    f_obj = get_object_or_404(Fundraiser, slug=fund_slug, active=True)
    if f_obj.ngo:
        if f_obj.ngo.icon:
            csologo = PHOTO_URL + "static" + f_obj.ngo.icon.url 
    myappeal = ""
    if f_obj.ngo:
        if f_obj.ngo.youtube_embedd:
            mmyappeal = f_obj.ngo.youtube_embedd +'?rel=0'
        else:
            myappeal = Link.objects.filter(content_type__model__iexact="event",object_id=event.id)
            if myappeal:
                myappeal = myappeal[0].URL+ '?rel=0'
    else:
        myappeal = Link.objects.filter(content_type__model__iexact="event",object_id=event.id)
        if myappeal:
            myappeal = myappeal[0].URL+ '?rel=0'

    champion_gold = get_badge_icon(f_obj)
    fundraiser_type = f_obj.fundraiser_type.name.replace("-","")    # champion details badge, icon black board message description , display name , myapeal, youtubelink, ngo, fundraiser type etc... querying from fundraiser table by eslug
    Care_champion_name = f_obj.created_by.first_name + " "+ f_obj.created_by.last_name
    Supporting_Cso_Description = strip_tags(f_obj.ngo.black_board_message) if f_obj.ngo.black_board_message else ""
    Cso_name = f_obj.ngo.name.replace("-" ,'') if f_obj.ngo else ""
    totalamount = f_obj.goal_amount if f_obj.goal_amount else 0
    DonatedAmount = int(f_obj.total_amount()) if f_obj.total_amount() else 0
    PercentageDonation = str(f_obj.percentage_donated()) + "%"
    ChampionLogo = PHOTO_URL +"static/" + f_obj.icon.url if f_obj.icon else PHOTO_URL +"/static/frontend/img/no-image.jpg"
    thanks_msg = Donation.objects.filter(active=True,fundraiser_id=f_obj.id,event_id=event.id,payment_status='Success').order_by('-id').values('thank_msg','first_name','id')[:3]
    return render(request,'frontend_templates/fundraisers_details.html', locals())


######## functions for the archive page #########
def get_event_dockets(doc):
  for i in doc:
    return i.attach_file.url

def get_single_event_video(obj):
  # function for getting single video of event
  for i in obj:
    return i.URL

def get_videos_for_event(self):
    return Link.objects.filter(content_type__model__iexact="event", object_id=self.id).order_by('?')[:1]

def get_event_ngo_count(obj):
  return NGO.objects.filter(event=obj,active=True).count()

def get_event_fundrasier_count(obj):
  return Fundraiser.objects.filter(event=obj,active=True,created_by__is_active=True).count()

def get_event_corporate_count(obj):
  return DuplicateCorporates.objects.filter(event=obj,active=True).count()


def total_amount_raised(self):
    directonlinedonation  = Donation.objects.filter(payment_status='Success', event=self,ngo=None).aggregate(total_amount=Sum('amount')).get("total_amount")
    directofflinedonation  = OfflineDonation.objects.filter( event=self,ngo=None).aggregate(total_amount=Sum('amount')).get("total_amount",0)
    if not directonlinedonation:
        directonlinedonation = 0
    if not directofflinedonation:
        directofflinedonation = 0

    total_ddonation = int(directonlinedonation) + int(directofflinedonation)

    tagged_ngos = self.ngo.all().values_list("id",flat=True)
    onlinedonation     = Donation.objects.filter(event=self, ngo_id__in=tagged_ngos, payment_status= "Success").aggregate(total_amount=Sum('amount')).get("total_amount",0)
    offlinedonation    = OfflineDonation.objects.filter(event=self, ngo_id__in=tagged_ngos).aggregate(total_amount=Sum('amount')).get("total_amount",0)

    if not onlinedonation:
        onlinedonation = 0
    if not offlinedonation:
        offlinedonation = 0
    total_donation    = int(onlinedonation) + int(offlinedonation)

    totalraised = total_ddonation + total_donation
    return totalraised



def archive(request):
    event=Event.objects.filter(active=True)
    #--------------------------Completed Event section
    completed_event =Event.objects.filter(event_type="marathon",end_date__gte=today,active=True).order_by('-end_date')
    completed_event_list = []
    [completed_event_list.append({'name':event.name,'image':PHOTO_URL + "static" + event.main_page_logo.url if event.main_page_logo else "" ,
                                  "event_key":event.slug,"slug":event.slug,
                                  "color":event.color,"video":get_single_event_video(event.get_videos_for_event()) if get_single_event_video(event.get_videos_for_event()) else "https://www.youtube.com/embed/Uka4r7t4Lic",
                                  "pdf":PHOTO_URL+get_event_dockets(event.get_event_dockets_annaul_reports())if get_event_dockets(event.get_event_dockets_annaul_reports()) else "",
                                  "cso_count":int(get_event_ngo_count(event)),
                                  'total_fundraised':event.total_amount_raised(),
                                  "share_image":PHOTO_URL + share_imageurl(event.widget_icon.url,'200x200') if event.widget_icon else '',
                                  "share_description":strip_tags(event.description),
                                  "share_title":event.name,
                                  "accept_donation":event.accept_donation,
                                  "fundraiser_count":int(get_event_fundrasier_count(event)),
                                  "corporate_count":int(get_event_corporate_count(event))}) for event in  completed_event] # default video hardcoded 
    #-----------------------

    #------------------------Campaign Completed section
    campaign_obj_completed = event.filter(event_type="campaign",end_date__lt=today)
    campaign_list_completed = []
    [campaign_list_completed.append({"corporate_count":int(get_event_corporate_count(event)),
                    "fundraiser_count":int(get_event_fundrasier_count(event)),
                    "cso_count":int(get_event_ngo_count(event)),
                    'name':event.name,'image':PHOTO_URL +"static" + event.main_page_logo.url if event.main_page_logo else "" ,
                    "event_key":event.slug,"slug":event.slug,"color":event.color,
                    "video":get_single_event_video(event.get_videos_for_event()) if get_single_event_video(event.get_videos_for_event()) else "https://www.youtube.com/embed/Uka4r7t4Lic",
                    "pdf":PHOTO_URL+ "static" + get_event_dockets(event.get_event_dockets_annaul_reports())if get_event_dockets(event.get_event_dockets_annaul_reports()) else ""}) for event in campaign_obj_completed]
    #----------------------- 
    #-----------------------Archive page Event Speak section 
    links = Link.objects.filter(active=True,content_type__model__iexact="event",object_id__in=Event.objects.filter(active=True).values_list('id',flat=True)).order_by('-id')
    link_list = []
    [link_list.append({'url':str (link.URL) + '?rel=0','text':str(link.name)})for link in links if link.URL]
    link_list = link_list[:3]
    #---------------------------
    return render(request,'frontend_templates/archive.html',locals())   


def event(request):
    return render(request,'frontend_templates/events.html',locals())   

############### for donation form.../after the clicking indian citizen button ###########

# @login_required(login_url='/login/')
def cso_donation_form(request, event_slug, cso_slug):
    """ Api for state_list"""
    state_list=[]
    state_obj = State.objects.filter(country=Country.objects.get(name='India'), active=True).order_by('name')
    [state_list.append({'id':state.id,'name':state.name})for state in state_obj]
    event = Event.objects.filter(slug=event_slug,active=True,end_date__gte=today)
    cso = NGO.objects.get(active=True, slug=cso_slug)
    terms_cond = Article.objects.get_or_none(slug='terms-and-condition-for-programs', active=True)
    if len(event) == 1:
        event = event.latest("created_on")
        accept_donation = event.accept_donation
        if not accept_donation:
            msg = "No donations are accepted for the {0} {1}.".format(event.event_type,event.name)
        else:
            msg = ""
    elif len(event) > 1:
        accept_donation = False
        msg = "Donations can not be made as muliple active event have same slug Please Contact Administrator. "
    else:
        accept_donation = False
        msg = "Page Not Found Please Contact Administrator."
    return render(request, "frontend_templates/cso_donate.html",locals())


################### donation function for fundraisers #####################################
# @login_required(login_url='/login/')
def fund_donation_form(request, event_slug, cham_slug):
    """ Api for state_list"""
    state_list=[]
    state_obj = State.objects.filter(country=Country.objects.get(name='India'), active=True).order_by('name')
    [state_list.append({'id':state.id,'name':state.name})for state in state_obj]

    event = Event.objects.filter(slug=event_slug,active=True,end_date__gte=today)
    cham = Fundraiser.objects.get(active=True, slug=cham_slug)
    terms_cond = Article.objects.get_or_none(slug='terms-and-condition-for-programs', active=True)
    if len(event) == 1:
        event = event.latest("created_on")
        accept_donation = event.accept_donation
        if not accept_donation:
            msg = "No donations are accepted for the {0} {1}.".format(event.event_type,event.name)
        else:
            msg = ""
    elif len(event) >1:
        accept_donation = False
        msg = "Donations can not be made as muliple active event have same slug Please Contact Administrator. "
    else:
        accept_donation = False
        msg = "Page Not Found Please Contact Administrator."
    return render(request, "frontend_templates/fundraiser_donate.html", locals())

############ this function for the donation next page #############
# @login_required(login_url='/login/')
def donation_form2(request, event_slug,cham_slug):
    event = Event.objects.get(active=True, slug=event_slug)
    # cso = event.ngo.get(active=True,slug=cso_slug)
    cham = Fundraiser.objects.get(active=True, slug=cham_slug)

    def post(self,request):
        key=request.data.get('key')#ngo,fundraiser
        slug=request.data.get('slug')#ngo swayam fundraiser Ruby
        eslug=request.data.get('eslug')#TSK25K
        amount=request.data.get('amount')
        pan_card_image = request.FILES.get("pan_card_image",None)
        # serializer = DonationSerializer(data=request.data)
        donation_obj = ''

        write_log(request.data,'NewDonationRegister()')

        # if serializer.is_valid():
        donation_obj=Donation.objects.create(txnid="",payment_status="",reciept_no="")
        donation_obj.thank_msg = request.data.get('thank_msg')
        card_type = request.data.get('card_type')
        if card_type == "PAN":
            donation_obj.pan_card = request.data.get('pan_card')
        else:
            donation_obj.pan_card = request.data.get('adhar_card')
        donation_obj.card_type = card_type    
        state_id = request.data.get('state')
        try:
            event_obj = Event.objects.get(slug=eslug,active=True)
            state_obj = State.objects.get(id=state_id)
            donation_obj.state = state_obj.name
            donation_obj.deduction_pecentage = event_obj.get_amount_deduction()
        except:
            pass
        if key == 'ngo':
            # import ipdb;ipdb.set_trace()
            if slug =='india-cares-foundation':
                ngo_obj = get_object_or_404(NGO, slug=slug, active=True)
            else:
                ngo_obj = get_object_or_404(NGO, slug=slug, active=True,event=event_obj)
            address = Address.objects.get(content_type=ContentType.objects.get(model__iexact='ngo'), object_id=ngo_obj.id)
            contact = NgoCommunication.objects.get(ngo=ngo_obj)
            desc_obj = EventNgoDescription.objects.filter(active=True,event__slug=str(eslug), ngo__slug=str(slug)).last()
            ngo_description = desc_obj
            if desc_obj:
                addrs = smart_text(smart_text(ngo_description.address1) + " " +smart_text(ngo_description.address2))
            else:
                addrs = 0
            tax = get_ngo_taxstatus(ngo_obj)
            donation_obj.ngo = ngo_obj
            if pan_card_image:
                donation_obj.pan_card_image = request.FILES['pan_card_image']
            contact_person_name =  str(ngo_obj.contact_person.user.first_name + " "+ngo_obj.contact_person.user.last_name)
            obj=get_donation_details(donation_obj,eslug,amount)
            donation_obj.deduction_pecentage = donation_obj.get_donation_deduction()
            if slug =='india-cares-foundation':
                contact_person_name = "Meena Dave"
                email  = "info@icfn.in"
            else:
                email = ngo_description.email if ngo_description else desc_obj.email if desc_obj else ngo_obj.contact_person.user.email


            return Response({"status":2,"message":"success","id":str(donation_obj.id),"logo": PHOTO_URL +ngo_obj.icon.url,
            "Mainheading":ngo_obj.name, "location":address.city,"tax_status":" ".join(tax),"Address_1":event_ngo_obj_data(address,ngo_description,'address1'),"city":event_ngo_obj_data(address,ngo_description,'city'),
            "state":event_ngo_obj_data(address,ngo_description,'state'),"country":event_ngo_obj_data(address,ngo_description,'country'),
            "pincode":event_ngo_obj_data(address,ngo_description,'pincode'),
            "contact_person":contact_person_name,"phone":event_ngo_obj_data(contact,ngo_description,'phone1'),"mobile":event_ngo_obj_data(contact,ngo_description,'mobile'),
            "website":event_ngo_obj_data(contact,ngo_description,'web_address'),"email":email,"txnid":obj[1][0],"net_bal":obj[1][1],"pay_bal":obj[1][2],"deduction_percentage":obj[1][3],"deduction_amount":obj[1][4]})
            
        elif key == 'fundraiser':
            # import ipdb; ipdb.set_trace()
            fundraiser = Fundraiser.objects.get_or_none(slug=slug, active=True,event=event_obj)
            # address = Address.objects.get(content_type=ContentType.objects.get(model__iexact='user'), object_id=fundraiser.created_by.id)# replaced with fundraiser id to 
            address = Address.objects.get(content_type=ContentType.objects.get(model__iexact='ngo'), object_id=fundraiser.ngo.id)
            contact = NgoCommunication.objects.get(ngo=fundraiser.ngo.id)
            tax = get_ngo_taxstatus(fundraiser.ngo)
            donation_obj.fundraiser = fundraiser
            donation_obj.ngo = fundraiser.ngo
            if pan_card_image:
                donation_obj.pan_card_image = request.FILES['pan_card_image']
            desc_obj = EventNgoDescription.objects.filter(event__slug=str(eslug), ngo__slug=str(donation_obj.ngo.slug)).last()
            ngo_description = desc_obj
            donation_obj.project = fundraiser.project
            contact_person_name =  str(fundraiser.ngo.contact_person.user.first_name+" "+ fundraiser.ngo.contact_person.user.last_name)
            obj=get_donation_details(donation_obj,eslug,amount)
            try:
                address_1 = str(address.address1)
            except:
                address_1 = address.address1.encode('ascii', 'ignore')
            donation_obj.deduction_pecentage = donation_obj.get_donation_deduction()
            return Response({"status":2,"message":"success","id":str(donation_obj.id),"logo": PHOTO_URL +fundraiser.ngo.icon.url,"country":str(address.country),"pincode": str(address.pincode),
            "contact_person":contact_person_name,"phone":contact.phone1 or contact.phone2,"mobile":address.mobile,
            "website":contact.web_address,"email":fundraiser.ngo.contact_person.user.email,"fundraiser_name":str(fundraiser.created_by.first_name+" "+ fundraiser.created_by.last_name),
            "Mainheading":fundraiser.display_name, "location":address.city,"tax_status":" ".join(tax),"Address_1":address_1,"city":str(address.city),"state":str(address.state),"txnid":obj[1][0],"net_bal":obj[1][1],"pay_bal":obj[1][2],"deduction_percentage":obj[1][3],"deduction_amount":obj[1][4]})
        

        if key == 'campaign':
            fundraiser = Fundraiser.objects.get_or_none(slug=slug, active=True,event=event_obj)
            ngo_obj = get_object_or_404(NGO, slug='india-cares-foundation', active=True)
            address = Address.objects.get(content_type=ContentType.objects.get(model__iexact='ngo'), object_id=ngo_obj.id)
            contact = NgoCommunication.objects.get(ngo=ngo_obj)
#                """desc_obj = EventNgoDescription.objects.get_or_none(event__slug=str(eslug), ngo__slug=str(slug))"""
            tax = get_ngo_taxstatus(ngo_obj)
            donation_obj.fundraiser = fundraiser
            donation_obj.ngo = ngo_obj
            if pan_card_image:
                donation_obj.pan_card_image = request.FILES['pan_card_image']
            contact_person_name =  str(ngo_obj.contact_person.user.first_name + " "+ngo_obj.contact_person.user.last_name)
            obj=get_donation_details(donation_obj,eslug,amount)
            try:
                address_1 = str(address.address1)
            except:
                address_1 = address.address1.encode('ascii', 'ignore')
            donation_obj.deduction_pecentage = donation_obj.get_donation_deduction()
            return Response({"status":2,"message":"success","id":str(donation_obj.id),"logo": PHOTO_URL +ngo_obj.icon.url,
            "Mainheading":event_obj.name, "location":address.city,"tax_status":" ".join(tax),"Address_1":address_1,"city":str(address.city),"state":str(address.state),"country":str(address.country),"pincode": str(address.pincode),
            "contact_person":contact_person_name,"phone":contact.phone1 or contact.phone2,"mobile":contact.mobile,
            "website":contact.web_address,"email":ICFN_INFO_MAIL,"txnid":obj[1][0],"net_bal":obj[1][1],"pay_bal":obj[1][2],"deduction_percentage":obj[1][3],"deduction_amount":obj[1][4]})
            

        else:
            return Response({"status":0,"message":"Key is mismatched"})
    return render(request, "frontend_templates/donate_page2.html", locals())


############ creating the fundraiser page ##############

# @login_required(login_url='/login/')
class ChooseCategory(View):
    def get(self, request, event_slug):
        data = request.GET
        csoid = data.get('cso_id')
        usr = request.user
        event = Event.objects.get(active=True, slug=event_slug)
        show_csodropdown = True
        if event.event_type == "Campaign":
            if event.campaign_type in ["CFC"]:#if the campign is with cso and fundraiser
                show_csodropdown = True
            else:
                show_csodropdown = False
        if usr:
            usr = User.objects.get(id=usr.id)
            alreadycreated = event.fundraisers.filter(created_by=usr,ngo__isnull=False).values_list("ngo",flat=True)
            ngo_obj = NGO.objects.filter(active=True,event=event,register_status=2).order_by('name').exclude(id__in=alreadycreated)
        else:
            ngo_obj = NGO.objects.filter(active=True,event=event,register_status=2).order_by('name')
        cat_list = event.allowed_categories.all()
        categories = FundraiserType.objects.filter(active=True, id__in=cat_list)
        cat_obj,download_form,slugs,min_pledge = [],[],[],[]
        for cat in categories.order_by('event_index'):
            if cat.get_fundraisertype_details():
                pledge_amount = cat.get_fundraisertype_details().enter_in_digits
                minimum_pledge = cat.get_fundraisertype_details().minimum_pledge
                download_formurl = ""
                if cat.get_fundraisertype_details().download_form:
                    download_formurl = PHOTO_URL+'/'+cat.get_fundraisertype_details().download_form.url
            else:
                pledge_amount = 0
                minimum_pledge = 0
                download_formurl = ""
            slugs.append({"slug":cat.slug,"id":cat.id,"pledgeamount":pledge_amount})
            cat_obj.append({"name":cat.name,"id":cat.id})
            download_form.append({"form":download_formurl,"id":cat.id})
            min_pledge.append({"min_pledge":minimum_pledge,"id":cat.id})
        return render(request, "frontend_templates/ChooseCategory.html", locals())
#--------------------------------------------

        
def events_awards(request, event_slug):
    event_obj = Event.objects.get(slug=event_slug,active=True)
    try:
        award_obj = EventAwards.objects.get(event=event_obj)
    except EventAwards.DoesNotExist:
        award_obj = None
    # featured_event_main = Event.objects.filter(active=True,end_date__gte=today,accept_donation=True,event_type='Marathon').order_by('id')[:2]
    return render(request, "frontend_templates/event_awards.html", locals())


def coming_soon(request):     
    return render(request,'frontend_templates/coming_soon.html',locals())   

def about_us(request):
    data = request.POST
    print(data)
    csoslug = data.get('csoslug')
    eslug = data.get('eslug')
    try:
        about_us = Section.objects.get(slug = 'about-us', active = True)
        about_us_vision = Article.objects.get(id=27,section = about_us, active=True)
        about_us_articles = Article.objects.filter(section = about_us, active=True).exclude(id=27)
        about_us_articles_upperpart = about_us_articles[0:3]
        about_us_articles_lowerpart = about_us_articles[3:6]
        staff = StaffType.objects.get(slug ='staff').get_staffs()
        trustee = StaffType.objects.get(slug ='trustees').get_trustees()
    except Exception as e:
        return Response({'status':0, 'message': 'somthing wrong', 'error': e.message})
    return render(request,'frontend_templates/about_us.html',locals())   

#@api_view(['POST'])
def contact_us(request):
    events = Event.objects.filter(active=True)
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-control'}))
    contact_us = get_object_or_404(Article, slug='contact-us', active=True)
    address = Address.objects.filter(content_type__model ="contactus",active=True)
    for detail in address:
        try:
            city_image = PHOTO_URL+ "static" +detail.city_image.url
        except:
            city_image = PHOTO_URL+ "static/no-image.jpg"

    # conatact us in this selected events email will get a mail
    # name , email, phone and message and receiver emails are selected events emails
    # subject mail is  A New Query on India Cares  will
    if request.method == 'POST':
        # import ipdb;ipdb.set_trace()
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')
        r_email = data['event']
        reciever_mail = [(get_object_or_404(Event,id=i).event_email,"") for i in r_email if r_email]
        Requests.objects.create(name=name, email=email, phone=phone, message=message)
        subject = 'A New Query on India Cares'
        msg = "The details of the Enquiry is as follows:"+"<br>"+"Name : "+name+"<br>"+"Email address : "+email+"<br>"+"Phone number : "+phone+"<br>"+"Enquiry : "+message
        send_sandgridmail(sender=email,receiver=reciever_mail,subject=subject,content=msg)
    return render(request,'frontend_templates/contact_us.html',locals())


################# function for the fundraising section ##############
def current_event_campaing(request):
    event=Event.objects.filter(active=True)
    #--------------------------Completed Event section
    marathon_obj_feature = event.filter(event_type="marathon",end_date__gte=today).order_by('-end_date')
    marathon_list_feature_list = []
    [marathon_list_feature_list.append({'name':event.name,'image':PHOTO_URL + "static" + event.main_page_logo.url if event.main_page_logo else "" ,
                                  "event_key":event.slug,"slug":event.slug,
                                  "color":event.color,"video":get_single_event_video(event.get_videos_for_event()) if get_single_event_video(event.get_videos_for_event()) else "https://www.youtube.com/embed/Uka4r7t4Lic",
                                  "pdf":PHOTO_URL+  get_event_dockets(event.get_event_dockets_annaul_reports())if get_event_dockets(event.get_event_dockets_annaul_reports()) else "",
                                  "cso_count":int(get_event_ngo_count(event)),
                                  "fundraiser_count":int(get_event_fundrasier_count(event)),
                                  "share_description":strip_tags(event.description),
                                  "share_title":event.name,
                                  "accept_donation":event.accept_donation,
                                  "share_image":PHOTO_URL + share_imageurl(event.widget_icon.url,'200x200') if event.widget_icon else '',
                                  "corporate_count":int(get_event_corporate_count(event))}) for event in marathon_obj_feature] # default video hardcoded
    #-----------------------

    #------------------------Campaign Completed section
    campaign_obj=event.filter(event_type="campaign",end_date__gte=today)
    campaign_list = []
    [campaign_list.append({"corporate_count":int(get_event_corporate_count(event)),
                                "fundraiser_count":int(get_event_fundrasier_count(event)),
                                "cso_count":int(get_event_ngo_count(event)),
                                'name':event.name,'image':PHOTO_URL + "static" + event.main_page_logo.url if event.main_page_logo else "" ,
                                "event_key":event.slug,"slug":event.slug,"color":event.color,
                                "video":get_single_event_video(event.get_videos_for_event()) if get_single_event_video(event.get_videos_for_event()) else "https://www.youtube.com/embed/Uka4r7t4Lic",
                                "pdf":PHOTO_URL+get_event_dockets(event.get_event_dockets_annaul_reports())if get_event_dockets(event.get_event_dockets_annaul_reports()) else ""}) for event in campaign_obj]
    #----------------------- 
    #-----------------------Archive page Event Speak section 
    links = Link.objects.filter(active=True,content_type__model__iexact="event",object_id__in=Event.objects.filter(active=True).values_list('id',flat=True)).order_by('-id')
    link_list = []
    [link_list.append({'url':str (link.URL) + '?rel=0','text':str(link.name)})for link in links if link.URL]
    link_list = link_list[:3]
    #---------------------------
    return render(request,'frontend_templates/current_event_campaing.html',locals())


######### for fundrasing pages ##############
def get_name_bold(a):
#This function is used for split the words and joining
    lis = a.split(' ')
    dict_obj = {}
    try:              
        dict_obj['name'] = lis[0] + ' ' + lis[1]
    except:
        dict_obj['name'] = lis[0]
    bold = lis[2:]
    b = ' '.join(bold)
    dict_obj['name2'] = b 
    return dict_obj['name'] , dict_obj['name2']

def make_fundraising(request):
    event = Event.objects.filter(display_in_joinus=True,active=True,feature_event=True).order_by('-id')
    if event:
        event_slug = event[0].slug
    else:
        event_slug = ""
    article_two = get_object_or_404(Article, slug='make-your-fundraising-page', active=True)
    make_name = get_name_bold(article_two.name)[0]
    make_name1 = get_name_bold(article_two.name)[1]
    return render(request,'frontend_templates/make_your_fundraising_page.html',locals()) 
#-------------------------------------------------------


# def articles(request,article_slug):
#     featured_event_main = Event.objects.filter(active=True,end_date__gte=today,accept_donation=True,event_type='Marathon').order_by('id')
#     if featured_event_main:
#         featured_event_main = featured_event_main[:2]
#     f_event = []
#     for obj in featured_event_main:
#         f_event.append({"id":obj.id,"slug":obj.slug,"image": PHOTO_URL + obj.join_us_logo.url if obj.join_us_logo else '',
#                         "share_image":obj.widget_icon.url if obj.widget_icon else '',
#                         "share_description":strip_tags(obj.description), "share_title":obj.name}) 
#     article_one = get_object_or_404(Article, slug=article_slug, active=True)
#     featured_event = Event.objects.filter(display_in_joinus=True,active=True, end_date__gte=today).order_by('-id')
#     return render(request, 'frontend_templates/articles.html',locals())


def get_name_split(a):
# this is used spiting the words
    lis = a.split(' ')
    dict_obj = {}              
    dict_obj['name'] = lis[0] + ' ' + lis[1] + ' ' +lis[2]
    bold = lis[3:]
    b = ' '.join(bold)
    dict_obj['name2'] = b 
    return dict_obj['name'] , dict_obj['name2']

def why_fundraise(request):
    event = Event.objects.filter(display_in_joinus=True,active=True,feature_event=True).order_by('-id')    
    featured_event_main = Event.objects.filter(active=True,end_date__gte=today,accept_donation=True,event_type='Marathon').order_by('id')[:2]
    length = len(featured_event_main)
    article_one = get_object_or_404(Article, slug='how-to-start-fundraising', active=True)
    if event:
        event_slug = event[0].slug
        print(event_slug)
    else:
        event_slug = ""
    start_name = get_name_split(article_one.name)[0]
    start_name1 = get_name_split(article_one.name)[1]
    return render(request,'frontend_templates/how_to_start_fundraisering.html',locals())                                      
#--------------------------------------------------------------
# my page function it's for when login user will create the fundraiser page
# from django.contrib.auth.decorators import login_required
# @login_required(login_url='/login/')
class FundraiserPageCreation(View):
######################## Creating Fundraiser Page ###############
    def get(self, request):
        event_slug = request.GET.get("eslug")
        choose_category = request.GET.get("choose_category")
        event = Event.objects.get(active=True, slug=event_slug)
        categories = FundraiserType.objects.filter(active=True, id=choose_category)
        for i in categories:
            if i.get_fundraisertype_details():
                goal = i.get_fundraisertype_details().enter_in_digits
            else:
                goal = 0
        if event.active == False:
            msg = "you can not create fundraiser page for this event"
        return render(request,'frontend_templates/fundraiser_page_creation.html',locals())

    def post(self,request):
        # import ipdb;ipdb.set_trace()
        data = request.POST
        query_param= request.GET
        fund_obj = ""
        sslug = ['i-pledgers', 'icare', 'isupport']
        eslug = query_param.get('eslug')
        event_obj = Event.objects.get(slug=eslug,active=True)
        ngo = query_param.get('csoslug')
        ngo_obj = NGO.objects.get(id=ngo)
        usr = request.user
        user_obj = User.objects.get(id=usr.id)
        fund_category = query_param.get('choose_category')
        if event_obj.event_type == 'Cyclothon':
            fund_category = 'i-pledgers'
        elif event_obj.event_type == 'Campaign':
            fund_category = 'icare'
        elif event_obj.slug == 'mysurumarathon' or event_obj.slug == 'RMM':
            fund_category = 'isupport'
        cat_obj = FundraiserType.objects.get_or_none(id=fund_category)
        ftitle = data.get('title')
        slug = slugify(data.get('slug'))
        description = data.get('editor1')
        thank_msg = data.get('thank_msg')
        if Fundraiser.objects.filter(slug=slug).exists():
            error = "This URL already exists"
        else:
            if not event_obj.is_eventdone():
                existingpage = event_obj.fundraisers.filter(ngo=ngo_obj,created_by=user_obj)
                if not existingpage:
                    fund_obj = Fundraiser.objects.create(title=ftitle, description=description, thank_msg=thank_msg,
                                                        slug=slug, ngo=ngo_obj,
                                                        goal_amount = (data.get('goal_amount')),
                                                        fundraiser_type = cat_obj, created_by=user_obj)
                    if request.FILES.get('icon'):
                        fund_obj.icon = request.FILES.get('icon')
                    fund_obj.display_name =  user_obj.first_name + " " +user_obj.last_name
                    fund_obj.active = False  #eval(data.get('active').capitalize())
                    fund_obj.save()
                    user_obj.is_active = True
                    user_obj.save()
                    if event_obj:
                        event_obj.fundraisers.add(fund_obj)
                        event_obj.save()
                    error = "appeal page created for the {0} successfuly".format(ngo_obj.name),fund_obj.id
                    return HttpResponseRedirect('/my-pages')
                else:
                    error = "Fundraising page is already created for"
            else:
                error = "Can not create a fundraiser page for event"
        return render(request, 'frontend_templates/fundraiser_page_creation.html',locals())



######### for listing the all pages details ##############
@login_required(login_url='/login/')
def my_page(request):
    # import ipdb;ipdb.set_trace()
    data = request.POST
    usr = request.user
    val = data.get('status')
    user = User.objects.get(id=usr.id)	
    fund_obj = Fundraiser.objects.filter(created_by=user)
    event = Event.objects.filter(active=True).latest('id')  
    if val == "0":
        fund_obj = fund_obj    
    elif val == "true":
        fund_obj =  fund_obj.filter(active=True, created_by=user) 
    elif val == "false":
        fund_obj =  fund_obj.filter(active=False, created_by=user)
    return render(request,'frontend_templates/my_page.html', locals()) 

############# for deactiveting the fundraiser page ################
def deactivet_fundraisesr_page(request):
    # import ipdb;ipdb.set_trace()
    data = request.POST
    fund_id = data.get('fund_id')
    print(fund_id)
    val_dict = {True:False,False:True}
    # fundraiser = Fundraiser.objects.get(id=fund_id)
    # val = data.get('status')
    # if val == False:
    #     today = datetime.datetime.today().date()
    #     end_date = fundraiser.event_set.filter(active=True).latest("created_on").end_date
    #     if today > end_date:
    #         msg = "Please create a new fundraiser page instead as this fundraiser page is for an old event"
    # fundraiser.active = val_dict[0]
    # if fundraiser.active == True:
    #     msg = "Deactivate"
    #     print(msg)
    # else:
    #     msg = "Active"
    #     print(msg)
    # fundraiser.save()
    # return render(render, 'frontend_templates/my-pages.html', locals())
    return HttpResponseRedirect('/my-pages')



##### user account details page #############
@login_required(login_url='/login/')
def my_account(request):
    event = Event.objects.filter(active=True)
    user_obj = request.user
    user_pic_obj = UserProfile.objects.get(user = user_obj)
    address = Address.objects.get_or_none(content_type__model='user', object_id=user_obj.id)
    donations = Donation.objects.filter(fundraiser__created_by_id=user_obj.id, payment_status='Success').count()
    fund_count = Fundraiser.objects.filter(created_by_id=user_obj.id).count()
    fund_list = Fundraiser.objects.filter(created_by_id=user_obj.id)
    add2 = address.address2 if address.address2 else "" 
    address_obj = str(address.address1 + ' '+add2 + ' '+address.city +' '+ address.pincode)
    amt = 0
    featured_event = Event.objects.filter(display_in_joinus=True,active=True,event_type="Marathon", end_date__gte=datetime.datetime.today()).order_by('-id')[0]
    if user_pic_obj.profile_pic:
        PHOTO_URL + user_pic_obj.profile_pic.url 
    else:
        PHOTO_URL +"/static/no-image.jpg",
    
    if user_obj.last_name:
        user_obj.first_name + ' ' +user_obj.last_name 
    else:
        ''
    for i in fund_list:
        amt = amt+i.total_amount()
    return render(request, 'frontend_templates/my_account.html', locals())


######## fundraiser details page ##################
@login_required(login_url='/login/')
def preview_page(request):
    # permission_classes = (IsAuthenticated,)
    # import ipdb;ipdb.set_trace()
    data = request.GET
    eslug = data.get('eslug')
    fslug = data.get('fslug')
    event_description = None
    event_obj = Event.objects.get(slug=eslug,active=True)
    fund_obj = Fundraiser.objects.get(slug=fslug)  
    try:
        event_description = EventNgoDescription.objects.get(event=event_obj, ngo=fund_obj.ngo)
    except:
        pass
    if fund_obj in event_obj.fundraisers.all():
        in_event = True
    else:
        in_event = False
    if fund_obj.ngo:
        ngoname = fund_obj.ngo.name
        black_board_message = fund_obj.ngo.black_board_message
        ngo_id = fund_obj.ngo.id
        if fund_obj.ngo.icon:
            ngo_icon = PHOTO_URL + "static" + fund_obj.ngo.icon.url
        else:
            ngo_icon = PHOTO_URL + "/static/no-image.jpg"
    else:
        ngoname = ""
        ngo_id = 0
        black_board_message = ""
        ngo_icon = PHOTO_URL +"/static/no-image.jpg"
    video = ""
    try:
        if event_description:
            video = event_description.youtube_embedd
    except:
        if fund_obj.ngo.youtube_embedd:
            video = fund_obj.ngo.youtube_embedd
    donation_count = int(fund_obj.get_donation_count())
    donated_amount = int(fund_obj.total_amount()) 
    percentage = fund_obj.percentage_donated()
    fund_icon = PHOTO_URL + "static" + fund_obj.icon.url if fund_obj.icon else PHOTO_URL +"/static/annaporna_2_EYFlicx.jpg"
    display_name = fund_obj.display_name or str(fund_obj.created_by.first_name + ' '+fund_obj.created_by.last_name)
    return render(request, 'frontend_templates/preview.html', locals())


#################### completion off creating fundraiser ##############
# after succesfully created Fundraiser 
# to making active 
# field True 
# with that fundraiser id
# fundraiser will activate
#######################################################################
@csrf_exempt
def CompleteFundraiserRegistration(request):
    data = request.POST
    fund_id = data.get('f_id')
    fund_obj = Fundraiser.objects.get(id=fund_id)
    fund_obj.active = True
    fund_obj.save()
    fundraiser_title = ""
    page_created_by = fund_obj.created_by
    uprof = UserProfile.objects.filter(user=page_created_by)
    gender = ""
    if uprof:
        fundraiser_title = uprof.latest("id").title.name
        # if fundraiser_title in [""]
    eslug = data.get('eslug')
    event_obj = Event.objects.get(slug=eslug,active=True)
#		# sub = "Fundraiser Page Created Successfully"
    sub = "User Created Successfully on India Cares Website"
    user_details_obj = UserDetails.objects.get_or_none(user=fund_obj.created_by)
    # actlink = HOST_URL+"/champion-details/"+eslug+"/"+fund_obj.slug+"/"+str(fund_obj.id)
    actlink = HOST_URL+eslug+"/fundraiser/"+fund_obj.slug
    # content = render_to_string('mailer2/fundraise_created.html',{
#  									'today': datetime.datetime.today(),
#  									'fund_obj': fund_obj,
#  									'actlink':actlink, 
#  									'user_details_obj':user_details_obj,
#  									'event_obj':event_obj
#  									})
    content = render_to_string('Archive/index5.html',{
                                'today': datetime.datetime.today(),
                                'fund_obj': fund_obj,
                                'actlink':actlink, 
                                'user_details_obj':user_details_obj,
                                'event_obj':event_obj
                                })
#	    		# sender_mail = "ADMIN_SENDER_MAIL"
    content_cso = render_to_string('Archive/funndraiser_created_cso_intimaion_mail.html',{
                                    'today':datetime.datetime.today(),
                                    'fund_obj': fund_obj,
                                    'user_details_obj':user_details_obj,
                                    'event_obj':event_obj,
                                    "fundraiser_title":fundraiser_title
                                    })
    sender_mail = ADMIN_SENDER_MAIL
    info_mail = ICFN_INFO_MAIL
    cso_sub = "Fundaraiser page has been created on your cso page"
    if fund_obj.ngo:
        DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(fund_obj), object_id=fund_obj.id,html="funndraiser_created_cso_intimaion_mail.html", mailtype="Registration", text="Fundraiser page created through event", sender=ADMIN_SENDER_MAIL, receiver=[fund_obj.created_by.email,], functionname="CompleteFundraiserRegistration()")	
        cso_smail = send_sandgridmail(sender=sender_mail,receiver=[(fund_obj.ngo.contact_person.user.email,"")],subject=cso_sub,content=content_cso,cc=[info_mail])

    DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(fund_obj), object_id=fund_obj.id,html="index5.html", mailtype="Registration", text="Fundraiser page created through event", sender=ADMIN_SENDER_MAIL, receiver=[fund_obj.created_by.email,], functionname="CompleteFundraiserRegistration()")
    smail = send_sandgridmail(sender=sender_mail,receiver=[(fund_obj.created_by.email,"")],subject=sub,content=content,cc=[info_mail])

    subject = "Account Details for "+ fund_obj.title + " at India Cares Foundation"
#					# message = get_message_for_mail(fund_obj)
    if fund_obj.ngo:
        message = "Hello Administrator," +"<br>"+ "A new fundraising page has registered at icfn.in."+ "<br>" +"This e-mail contains their details:"+"<br>"+"Name: "+fund_obj.created_by.first_name+"\n"+"Title: "+fund_obj.title+"\n"+"NGO: "+fund_obj.ngo.name +"<br>"+"Please do not respond to this message. It is automatically generated and is for information purposes only."
    else:
        message = "Hello Administrator," +"<br>"+ "A new fundraising page has registered at icfn.in."+ "<br>" +"This e-mail contains their details:"+"<br>"+"Name: "+fund_obj.created_by.first_name+"\n"+"Title: "+fund_obj.title+"\n"+"Please do not respond to this message. It is automatically generated and is for information purposes only."
#			    # receiver_mail = [ADMIN_SENDER_MAIL,]
    receiver_mail = [(RECEIVER_MAIL,"")]
    DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(fund_obj), object_id=fund_obj.id,html="fundraise_created.html", mailtype="AdminMails", text="Admin mail for fundraiser page created through event", sender=ADMIN_SENDER_MAIL, receiver=receiver_mail, functionname="CompleteFundraiserRegistration()")
    send_sandgridmail(sender=sender_mail,receiver=receiver_mail,subject=subject,content=message)
    return JsonResponse({"status":2,'message':"successfully registered click here to view your page"})
    # return render(request,'frontend_templates/fundraisers_details.html', locals())
    # return HttpResponseRedirect('/{{ eslug }}/fundraiser/{{ fslug }}')





############# edit function for edit form to edit in the fundraiser page ################### 
@login_required(login_url='/login/')
def fundraiser_page_edit(request):
    # import ipdb;ipdb.set_trace()
    data = request.POST
    fund_id = data.get('fund_id')
    fund_obj = Fundraiser.objects.get(id=fund_id)
    fund_obj.title = data.get('title')
    fund_obj.description = data.get('editor1')
    fund_obj.thank_msg = data.get('thank_msg')
    fund_obj.display_name = data.get('display_name')
    fund_obj.goal_amount = int(data.get('goal_amount'))
    if request.FILES.get('icon'):
        fund_obj.icon=request.FILES['icon']
    fund_obj.save()
    return HttpResponseRedirect('/my-pages')



##### user account details page #############
def my_account(request):
    event = Event.objects.filter(active=True)
    user_obj = request.user
    user_pic_obj = UserProfile.objects.get(user = user_obj)
    address = Address.objects.get_or_none(content_type__model='user', object_id=user_obj.id)
    donations = Donation.objects.filter(fundraiser__created_by_id=user_obj.id, payment_status='Success').count()
    fund_count = Fundraiser.objects.filter(created_by_id=user_obj.id).count()
    fund_list = Fundraiser.objects.filter(created_by_id=user_obj.id)
    add2 = address.address2 if address.address2 else "" 
    address_obj = str(address.address1 + ' '+add2 + ' '+address.city +' '+ address.pincode)
    amt = 0
    featured_event = Event.objects.filter(display_in_joinus=True,active=True,event_type="Marathon", end_date__gte=datetime.datetime.today()).order_by('-id')[0]
    if user_pic_obj.profile_pic:
        PHOTO_URL + user_pic_obj.profile_pic.url 
    else:
        PHOTO_URL +"/static/cso-banner-new.jpg",
    
    if user_obj.last_name:
        user_obj.first_name + ' ' +user_obj.last_name 
    else:
        ''
    for i in fund_list:
        amt = amt+i.total_amount()
    return render(request, 'frontend_templates/my_account.html', locals())


# class FundraiserResetPassword(APIView):
# 	permission_classes = (IsAuthenticated,)
# 	def post(self,request):
# 		user_id = request.data.get('user_id')
# 		serializer = PasswordSerializer(data=request.data)
# 		if serializer.is_valid():
# 			username = User.objects.get(id=user_id)
# 			user_obj= authenticate(username=username.username, password=request.data['old_password'])
# 			if user_obj:
# ## USerdetails table updat
# 				UserDetails.objects.filter(user_id=user_id).update(password=request.data.get('password'))
# 				user_obj.set_password(request.data.get('password'))
# 				user_obj.save()
# 				response = {"status":2,"message":"Password reset Done"}				
# 			else:
# 				response = {"status":0,"message":"Please enter correct old password"}
# 		else:
# 			response = serializer.errors
# #			 # = {"status":0,"message":error}
# 		return Response(response)




######## fundraiser details page ##################
def preview_page(request):
    # permission_classes = (IsAuthenticated,)
    # import ipdb;ipdb.set_trace()
    data = request.GET
    print(data)    
    usr = request.user
    eslug = data.get('eslug')
    fslug = data.get('fslug')
    event_description = None
    event_obj = get_object_or_404(Event,slug=eslug,active=True)
    fund_obj = get_object_or_404(Fundraiser, slug=fslug)
    try:
        event_description = EventNgoDescription.objects.get(event=event_obj, ngo=fund_obj.ngo)
    except:
        pass
    if fund_obj in event_obj.fundraisers.all():
        in_event = True
    else:
        in_event = False
    if fund_obj.ngo:
        ngoname = fund_obj.ngo.name
        black_board_message = fund_obj.ngo.black_board_message
        ngo_id = fund_obj.ngo.id
        if fund_obj.ngo.icon:
            ngo_icon = PHOTO_URL + fund_obj.ngo.icon.url
        else:
            ngo_icon = PHOTO_URL +"/static/frontend/img/no-image.jpg"
    else:
        ngoname = ""
        ngo_id = 0
        black_board_message = ""
        ngo_icon = PHOTO_URL +"/static/frontend/img/no-image.jpg"
    video = ""
    try:
        if event_description:
            video = event_description.youtube_embedd
    except:
        if fund_obj.ngo.youtube_embedd:
            video = fund_obj.ngo.youtube_embedd
    # response = {"ngo_name":ngoname,"title":fund_obj.title,
    #             "display_name":fund_obj.display_name or str(fund_obj.created_by.first_name + ' '+fund_obj.created_by.last_name),
    #             "description":fund_obj.description[:200] + '...',"description_read_more":fund_obj.description,"ngo_icon":ngo_icon,
    #             "fundraiser_type":fund_obj.fundraiser_type.name,"fund_icon":PHOTO_URL +fund_obj.icon.url if fund_obj.icon else PHOTO_URL +"/static/frontend/img/no-image.jpg",
    #             "black_board_message":black_board_message,"goal_amount":fund_obj.goal_amount,
    #             "donation_count":int(fund_obj.get_donation_count()),"donated_amount":int(fund_obj.total_amount()),"percentage":fund_obj.percentage_donated(),
    #             "video":video,"fund_id":fund_obj.id,
    #             "fundraiser_in_event":in_event,"eslug":event_obj.slug,"ngo":ngo_id,"slug":fund_obj.slug,"fundraiser_type_slug":fund_obj.fundraiser_type.slug}
    return render(request, 'frontend_templates/preview.html', locals())



def for_corporate(request):
    offer_obj = Article.objects.get_or_none(slug='for-corporate', active=True)   
    return render(request,'frontend_templates/for_corporate.html',locals()) 

def cso_adhm(request):     
    return render(request,'frontend_templates/cso.html',locals())

def events_adhm(request):     
    return render(request,'frontend_templates/events_adhm.html',locals()) 

def events_tsk(request):     
    return render(request,'frontend_templates/events_tsk25k.html',locals())

def campaigns_water_maharashtra(request):     
    return render(request,'frontend_templates/campaign_detail.html',locals())  

def for_cso(request):
    forcso = Article.objects.get_or_none(slug='for-csos', active=True)   
    return render(request,'frontend_templates/what_we_offer_for_cso.html',locals())   

def cso_tsk(request):     
    return render(request,'frontend_templates/cso_tsk.html',locals())

def fundraisers_adhm(request):     
    return render(request,'frontend_templates/fundraisers_adhm.html',locals())

def fundraisers_tsk(request):     
    return render(request,'frontend_templates/fundraisers_tsk.html',locals()) 

def faq(request):
    ##########################____faq____############################
    # for getting the all question and answer for all faqs
    faq_cat = FaqCategory.objects.filter(choice='main',is_active=True).order_by('name')
    events = Event.objects.filter(event_type__in=['Marathon','Campaign'],active=True).values('name','event_email')
    if request.method == 'POST':
        import ipdb;ipdb.set_trace()
        data = request.POST
        name = data.get('name')
        message = data.get('message')
        email = data.get('email')
        phone = data.get('phone')
        request_obj = Requests.objects.create(name=name, email=email, phone=phone, message=message)
        subject = 'A New Request on India Cares '
        reciever_mail=[ADMIN_SENDER_MAIL,]
        reciever_mail=[request.data.get('sender_email'),]
        msg = "The details of the Enquiry is as follows:"+"<br>"+"Name : "+name+"<br>"+"Email address : "+email+"<br>"+"Phone number : "+phone+"<br>"+"Enquiry : "+message
        DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(request_obj), object_id=request_obj.id,html="requests.html", mailtype="AdminMails", text="Request for India cares", sender=ADMIN_SENDER_MAIL, receiver=[ADMIN_SENDER_MAIL,], functionname="faq()")
        sub = "FAQ Requests on icfn"
        content = render_to_string('Archive/index12.html',{'name':name,'today':today})
        sender_mail = ADMIN_SENDER_MAIL
        mail = send_sandgridmail(sender_mail,[(email,"")],subject,content)
        return HttpResponseRedirect('/faq')
    return render(request,'frontend_templates/faq.html',locals())


def refund_policy(request): 
    refund_policy=  Article.objects.get_or_none(slug='refund-policy', active=True)    
    return render(request,'frontend_templates/refund_policy.html',locals())

def privacy_policy(request):
    privacy_policy=  Article.objects.get_or_none(slug='privacy-policy', active=True)
    return render(request,'frontend_templates/privacy_policy.html',locals())  

def terms_conditions(request):
    terms_cond = Article.objects.get_or_none(slug='terms-and-condition-for-programs', active=True)
    # terms_cond = Article.objects.get_or_none(slug='terms-and-conditions', active=True)
    return render(request,'frontend_templates/terms_conditions.html',locals())  


def cso_signup(request):
    ngos = NGO.objects.filter(active=True,register_status=2)
    if request.method == 'POST':
        # import ipdb;ipdb.set_trace()
        ngo_list = request.POST.get('ngo_list')
        title = request.POST.get('title')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        response = ''

        ngo = NGO.objects.get_or_none(id=ngo_list)
        if email == ngo.contact_person.user.email:
            subject = "You have been requested to change password!"
            sender_mail = ADMIN_SENDER_MAIL #SENDER_MAIL
            actlink = HOST_URL + '/forgot-password/'
            ngo_msg = render_to_string('mailer/request_for_password_change_cso.html',{'title':title,'today':datetime.datetime.today(), 'first_name': fname, 'last_name':lname, 'actlink':actlink})
            email = send_sandgridmail(sender=SENDER_MAIL,receiver=RECEIVER_MAIL,subject=subject,content=ngo_msg,reply_to=sender_mail)
            response = "Please check mail for more information"
        else:
            uid = uuid4().hex[:20]
            checkcso_obj, created = CheckCSO.objects.get_or_create(cso=ngo, email=email)
            checkcso_obj.first_name = fname
            checkcso_obj.last_name = lname
            if created:
                checkcso_obj.uid = uid
                checkcso_obj.mobile = mobile
                checkcso_obj.save()
                subject = "User has requested for access!"
                sender_mail  = RECEIVER_MAIL
            # try:
            receiver_mail = [ (RECEIVER_MAIL,"")]
            subject = "User has requested for access!"
            sender_mail  = RECEIVER_MAIL
            actlink = ''
            ngo_msg =  render_to_string('Archive/index15.html',{'title':title,'first_name':fname,'email':email,'mobile':mobile,'today': datetime.datetime.today(), 'obj': checkcso_obj, 'ngo':ngo, 'actlink':actlink})
            email = send_sandgridmail(sender=sender_mail,receiver=receiver_mail,subject=subject,content=ngo_msg,reply_to=sender_mail)
            DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(checkcso_obj), object_id=checkcso_obj.id,html="request_for_access_to_cso.html", mailtype="AdminMails", text="Admin mail for cso requests", sender=ADMIN_SENDER_MAIL, receiver=[RECEIVER_MAIL,], functionname="CsoRegistration()")
            response = "Thank you for providing your details, India Cares will approve your access to register within a few hours and you will get your password to complete registration for your CSO."    
            # except Exception as e:
            #     response = {'status':0, 'message': e.message}
            
        #return Response({"status":2,"message":response})
        return HttpResponseRedirect('/cso-signup')
    return render(request,'frontend_templates/cso_signup.html',locals())

########### if user forget the password and want to change the password ####################
def change_password(request):
    # password reset email is input field
    # if email is present in user table
    # it will send the token and uid to that particular mail
    user = request.POST.get('email')
    # import ipdb;ipdb.set_trace()
    if User.objects.filter(username=user).exists():
        username = User.objects.get(username=user)
        actlink =  HOST_URL+"/reset-password/" + urlsafe_base64_encode(force_bytes(username.pk))+'/'+default_token_generator.make_token(username) 
        msg = "Dear "+ username.first_name +"<br>"+"You have requested a new password for your account on  https://icfn.in/" +"<br>"+"The forget password link:"+"<br>"+"username : "+username.username+"<br>"+"Email address : "+username.email+"<br>"+"password link :"+actlink +"<br>"+"We thank you for your continuing support to the cause or causes you believe in."
        sender_mail = ADMIN_SENDER_MAIL
        subject = 'Password reset Request '
        content =  render_to_string('Archive/index4.html',{'today': datetime.datetime.today(), 'user_obj': username,'actlink':actlink})
        send_sandgridmail(sender=sender_mail,receiver=[(user,"")],subject=subject,content=content,reply_to=sender_mail)
        Response = "Please Check Your Mail"
    else:
        Response = "This Email Does Not Exist, Please Register"
    return render(request, 'frontend_templates/change_password.html', locals())



def cso_registration(request):
    countries=Country.objects.filter(active=True)
    # states=State.objects.all()
    cause=Cause.objects.filter(active=True)
    events = Event.objects.filter(active=True)
    slutations = Salutations.objects.filter(active=True)

    # if cso is logged in get the detail if present to show in the detail pages
    if request.user.is_authenticated:
        user_obj = User.objects.get(id=request.user.id)
        # user_profile_obj = UserProfile.objects.get(user=user_obj)
        user_profile_obj = UserProfile.objects.filter(user_id=user_obj).latest('id')
        ngo = NGO.objects.get(contact_person_id=user_profile_obj.id)
        print(ngo.id)
        ngo_comm = NgoCommunication.objects.get(ngo_id=ngo.id)            
        address = Address.objects.get(content_type=ContentType.objects.get(model__iexact='ngo'),object_id = ngo.id)  
        state = ""
        country = "" 
        mobile   = address.mobile
        address1 = address.address1
        address2 = address.address2
        city     = address.city
        pincode  = address.pincode
        if address.state:
            state    = address.state.id
        if address.country:
            country  = address.country.id
        cso_name = ngo.name
        landline = ngo_comm.phone1
        year_founded       = datetime.datetime.strftime(ngo.established_on,"%d/%m/%Y")
        if ngo.icon:
            logo               = ngo.icon.url
        else:
            logo = ""

        if ngo.audited_balance_sheet:
            balance_sheet = ngo.audited_balance_sheet.url
        else:
            balance_sheet = ""
        
        if ngo.profit_loss_statement:
            profit_loss = ngo.profit_loss_statement.url
        else:
            profit_loss = ""

        if ngo.g80_receipt:
            g_approval = ngo.g80_receipt.url
        else:
            g_approval = ""

        if ngo.a12_receipt:
            a_approval = ngo.a12_receipt.url
        else:
            a_approval = ""

        if ngo.fcra_receipt:
            fcra_applicable = ngo.fcra_receipt.url
        else:
            fcra_applicable = ""

        if ngo.pan_card:
            pan_card = ngo.pan_card.url
        else:
            pan_card = ""
        fcra = ngo.fcra

        tagged_event = list(ngo.event_set.all().values_list("id",flat=True))
        if tagged_event:
            event = tagged_event[-1]
        else:
            event = ""

        if ngo.cause:
            primary_cause      = ngo.cause.id
        else:
            primary_cause  = ""
        mission            = ngo.our_mission
        webstie            = ngo_comm.web_address
        own_url            = ngo.slug
        youtube_url        = ngo.youtube_embedd
        fundraising_target = ngo.goal_amount,
        our_work           = ngo.work_acheivement 
        requirement        =  ngo.fund_utilisation_statement
        we_believe         = ngo.black_board_message
        #     mobile ,address1 ,address2 ,city ,pincode ,state ,country  ,cso_name ,landline,year_founded , logo ,primary_cause , mission , webstie ,own_url , youtube_url , fundraising_target , our_work , requirement , we_believe = "","","","","","","","","","","","","","","","","","","",""

        #Level 1 Details of the CSO
        level_one_data = { "title":user_profile_obj.title.id , "fname":user_obj.first_name, "lname":user_obj.last_name,
                            "email":user_obj.email,"mobile":mobile}
        level_one_data = json.dumps(level_one_data)
        #------------------------------------------------

        #Level 2 Details of the CSO
        level_two_data = {"address1":address1,"address2":address2,"city":city,"pincode":pincode,"state":state,
                          "country":country,"cso_name":cso_name,"landline":landline,"year_founded":year_founded,
                          "logo":logo,"primary_cause":primary_cause,"secondary_cause":"","mission":mission,
                          "webstie":webstie,"own_url":own_url,"youtube_url":youtube_url,"fundraising_target":fundraising_target,
                          "our_work":our_work,"requirement":requirement,"we_believe":we_believe
                          }
        level_two_data = json.dumps(level_two_data)
        #--------------------------------------------------
        # Level 3 Details
        level_three_data = {"balance_sheet":balance_sheet,"profit_loss":profit_loss,"g_approval":g_approval,
                            "a_approval":a_approval,"fcra_applicable":fcra_applicable,"pan_card":pan_card,
                            "fcra":fcra,"event":event}
        level_three_data = json.dumps(level_three_data)

        #---------------------------------------------------------------
        print(level_three_data)
    return render(request,'frontend_templates/cso_registration.html',locals())  


def cso_reg_level_one(request):
    if request.method == 'POST':
        # import ipdb;ipdb.set_trace()
        title = request.POST.get('title')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user_obj=''
        lname = lname if lname else ''
        if not User.objects.filter(username=email).exists():
            user_obj = User.objects.create_user(username=email,email=email,password=password1,first_name=fname,last_name=lname,is_active=False)
        else:
            try:
                if NGO.objects.filter(contact_person_id__user=User.objects.get(username=email).id).latest('id').register_status == 0:
                    user_obj = User.objects.get(username=email)
                    user_obj.email = email
                    user_obj.password=password1
                    user_obj.first_name=fname
                    user_obj.last_name=lname
                    user_obj.is_active=False
                    user_obj.save()
                else:
                    msg = "This Email Is Already Exists"
                    return render(request,'frontend_templates/cso_registration.html',locals())
            except:
                msg = "This Email Is Already Exists"
                return render(request,'frontend_templates/cso_registration.html',locals())

        user_profile_obj = UserProfile.objects.create(user=user_obj, usertype='1',title_id=title)
        UserDetails.objects.create(user=user_obj, password=password1, username=email)
        ngo = NGO.objects.create(contact_person_id=user_profile_obj.id,established_on=datetime.datetime.today(),secondary_focus='Education',register_status=3)            
        Address.objects.create(mobile=mobile,content_type=ContentType.objects.get(model__iexact='ngo'),object_id = ngo.id)                        
        NgoCommunication.objects.create(mobile=mobile,ngo_id=ngo.id)
        activation_key = userid()
        individual_activate = IndividualActivation(user=user_obj,activation_key=activation_key)
        individual_activate.save()
        actlink = HOST_URL+ "activate-user/?activation_key="+str(activation_key)
        sub = "User Registered Successfully on India Cares Website"
        content =  render_to_string('Archive/new_csor_registrations.html',{'today': datetime.datetime.today(), 'user_obj': user_obj,'title':user_profile_obj.title,'password':password1,'actlink':actlink})
        sender_mail = ADMIN_SENDER_MAIL #SENDER_MAIL
        DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(user_obj), object_id=user_obj.id,html="user_registration.html", mailtype="Registration", text="User registration", sender=ADMIN_SENDER_MAIL, receiver=[RECEIVER_MAIL,], functionname="CsoregistrationFirst()")
        smail = send_sandgridmail(sender=sender_mail,receiver=[(user_obj.email,"")],subject=sub,content=content,reply_to=sender_mail)
        user_id = user_obj.id
        ngo_id = ngo.id
        msg = "Successfully Registered. Please check your mail and activate your account to proceed to the next step"
    return render(request,'frontend_templates/cso_registration.html',locals())



''' Login in Required for the level 2 Registeration '''
@login_required(login_url='/login/')
def cso_reg_level_two(request):
    #cause=Cause.objects.all()
    if request.method == 'POST':
        # import ipdb;ipdb.set_trace()
        #edit = request.POST.get('edit')
        user_id = request.POST.get('user_id')
        ngo_id = request.session.get('ngo_id')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        landline = request.POST.get('landline')
        cso_name = request.POST.get('cso_name')
        year_founded = datetime.datetime.strptime(request.POST.get('year_founded'),'%m/%d/%Y') 
        logo = request.FILES.get('logo')
        primary_cause = request.POST.get('primary_cause')
        secondary_cause = request.POST.get('secondary_cause')
        mission = request.POST.get('mission')
        webstie = request.POST.get('webstie')
        own_url = request.POST.get('own_url')
        youtube_url = request.POST.get('youtube_url')
        fundraising_target = request.POST.get('fundraising_target')
        our_work = request.POST.get('our_work')
        requirement = request.POST.get('requirement')
        we_believe = request.POST.get('we_believe')

        try:
            user_id = user_id
            user_profile_id = UserProfile.objects.filter(user_id=user_id).latest('id').id
            if not NGO.objects.filter(slug=slugify(request.POST.get('own_url'))).exclude(id=ngo_id).exists():
                ngo_object = NGO.objects.get(contact_person_id=user_profile_id)
                ngo_comm = NgoCommunication.objects.get(ngo_id=ngo_object.id)
                country_obj = Country.objects.get(id=country,active=True)
                state_obj   = State.objects.get(id=state,country=country_obj)
                address_obj = Address.objects.get(content_type=ContentType.objects.get(model__iexact='ngo'),object_id = ngo_object.id)
                address_obj.address1=address1
                address_obj.address2=address2
                address_obj.city=city
                address_obj.pincode=pincode
                address_obj.state=state_obj
                address_obj.country=country_obj
                address_obj.save()
                cause_obj = Cause.objects.get(id=primary_cause)
                ngo_object.name=cso_name
                ngo_object.established_on=year_founded
                if not logo == '':
                    ngo_object.icon = logo
                ngo_object.cause=cause_obj
                ngo_object.our_mission=mission
                ngo_object.work_acheivement=our_work
                ngo_object.youtube_embedd=youtube_url
                ngo_object.slug=slugify(request.POST.get('own_url'))
                ngo_object.fund_utilisation_statement=requirement
                ngo_object.black_board_message=we_believe
                ngo_object.a12 = 'VA'
                ngo_object.goal_amount = fundraising_target
                ngo_object.validity_80G = 'VA'
                ngo_object.frontend_registered = True
                ngo_object.for_every_month_report = True
                ngo_object.for_fundraise_page = True
                ngo_object.for_donate_mail = True
                ngo_object.already_activated = False

                # if edit == '0':
                #     ngo_object.active = False
                #     ngo_object.register_status = 1

                ngo_object.save()
                ngo_comm.web_address=webstie
                ngo_comm.phone1=landline
                ngo_comm.save()

                #will work on saving on the secondary causes later

                    # sec_cause_obj = secondary_cause.split(',')
                    # for obj in sec_cause_obj:
                    #     cause_obj = Cause.objects.get(id=obj)
                    #     ngo_object.secondary_cause.add(cause_obj)
                
                #-----------------------------------
                level2_msg = "Successfully Added the Contact Details"
            else:
                # response = {"status":0,"message":[{"India cares url":"Your India Cares Url Already Exist"}]}
                level2url_msg = "Your India Cares Url Already Exist"
                return render('frontend_templates/cso_registeration.html',locals())
            
        except Exception as e:
            #response = {"status":0,"message":e.message}
            level2_msg = e.args[0]

    return HttpResponseRedirect('/cso-registration/')

    
''' Login in Required for the level 3 Registeration '''
@login_required(login_url='/login/')
def cso_reg_level_three(request):
    if request.method == "POST":
        # import ipdb;ipdb.set_trace()
        user_id = request.POST.get('user_id')
        user_profile_id = UserProfile.objects.filter(user_id=user_id).latest('id').id
        ngo_object = NGO.objects.get(contact_person_id=user_profile_id)
        balance_sheet         = request.FILES.get('balance_sheet')
        profit_loss_statement = request.FILES.get('profit_loss')
        g80_receipt           = request.FILES.get('80g_approval')
        a12_receipt          = request.FILES.get('12a_approval')
        fcra                  = request.POST.get('fcra')
        pan_card              = request.FILES.get('pan_card')
        fcra_applicable       = request.FILES.get('fcra_applicable')
        event                 = request.POST.get('event')

        if ngo_object.register_status == 2: #Success  If CSO is already Registered then then cso wiill be editing the details thus mail won't go
            if balance_sheet:
                ngo_object.audited_balance_sheet = balance_sheet
            if profit_loss_statement:
                ngo_object.profit_loss_statement = profit_loss_statement
            if g80_receipt:
                ngo_object.g80_receipt = g80_receipt
            if a12_receipt:
                ngo_object.a12_receipt  = a12_receipt
            if fcra_applicable:
                ngo_object.fcra_receipt = fcra_applicable
            if pan_card :
                ngo_object.pan_card  = pan_card
            ngo_object.register_status = 2
            ngo_object.fcra      = request.POST.get("fcra")
            ngo_object.display_in_main = True
            ngo_object.frontend_registered = True
            ngo_object.save()
            try:
                event_obj = Event.objects.get(id=event)
#                # event_obj.ngo.add(ngo_object)
                event_obj.ngo.remove(ngo_object)
                event_obj.ngo.add(ngo_object)
                event_obj.save()
            except:
                pass
            response_msg = "Successfully Updated"
        else: # If NGO registeration status is not success mail will go the Admin on the succesfull Regiseration
            if balance_sheet:
                ngo_object.audited_balance_sheet = balance_sheet
            if profit_loss_statement:
                ngo_object.profit_loss_statement = profit_loss_statement
            if g80_receipt:
                ngo_object.g80_receipt = g80_receipt
            if a12_receipt:
                ngo_object.a12_receipt  = a12_receipt
            if fcra_applicable:
                ngo_object.fcra_receipt = fcra_applicable
            if pan_card:
                ngo_object.pan_card  = pan_card
            ngo_object.register_status = 2
            ngo_object.fcra      = request.POST.get("fcra")
            ngo_object.display_in_main = True
            ngo_object.frontend_registered = True
            ngo_object.active = True
            ngo_object.save()
            try:
                event_obj = Event.objects.get(id=event)
                event_obj.ngo.add(ngo_object)
            except:
                pass
            sub = "CSO Registered Successfully on India Cares Website"
            content = render_to_string('Archive/index3.html',{'today': datetime.datetime.today(), 'ngo_obj': ngo_object, 'password':UserDetails.objects.filter(user_id=user_id).latest('id').password,})
            sender_mail = ADMIN_SENDER_MAIL #SENDER_MAIL
            DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(ngo_object), object_id=ngo_object.id,html="ngo_registration.html", mailtype="Registration", text="NGO mail for registration", sender=ADMIN_SENDER_MAIL, receiver=[ngo_object.contact_person.user.email,], functionname="add_cso()")
            smail = send_sandgridmail(sender=sender_mail,receiver=[(ngo_object.contact_person.user.email,"")],subject=sub,content=content,reply_to=sender_mail)
            subject = "Account Details for "+ ngo_object.contact_person.user.first_name + " at India Cares Foundation"
            message = "Hello Administrator," +"<br>"+ "A new CSO has registered at icfn.in."+ "<br>" +"This e-mail contains their details:"+"<br>"+"Name: "+ngo_object.contact_person.user.first_name+"<br>"+"E-mail: "+ngo_object.contact_person.user.email+"<br>"+"CSO Name: "+ngo_object.name+"<br>"+"Please do not respond to this message. It is automatically generated and is for information purposes only."
            receiver_mail = [ (RECEIVER_MAIL,"")]
            DoantionMailer.objects.create(content_type=ContentType.objects.get_for_model(ngo_object), object_id=ngo_object.id,html="ngo_registration.html", mailtype="AdminMails", text="Admin mail for ngo registration", sender=ADMIN_SENDER_MAIL, receiver=RECEIVER_MAIL, functionname="CsoregistrationThird()")
            send_sandgridmail(sender=sender_mail,receiver=receiver_mail,subject=subject,content=message)
            response_msg = "Thank You for Registering with India Cares. Your Page Will Be Active Within 48 Hours after the Verification of All the Documents Submitted and Content Provided."
    return HttpResponseRedirect('/cso-registration/') 



def get_champion_badge(f_obj):
	########### Badge function #############################
	# Diamond
	# Platinum
	# Gold
	# Silver 
	# icare

	# badges returning on the basis of 
	# fundraiser type badges are returning 
	######################################################## 
    champion_gold = ""
    if 'Diamond' in f_obj.name:
        champion_gold =  PHOTO_URL +"/static/images/icon/diamond.png"
    elif 'Gold' in f_obj.name:
        champion_gold = PHOTO_URL + "/static/images/icon/champion_gold.png"
    elif 'Platinum' in f_obj.name:
        champion_gold = PHOTO_URL + "/static/images/icon/platinum.png"
    elif 'Silver' in f_obj.name:
        champion_gold =  PHOTO_URL +"/static/images/icon/silver.png"
    else:
        champion_gold =  PHOTO_URL +"/static/images/icon/icare_badge.png"
    return champion_gold



def fundraisers_type_listing(request,event_slug,id):
    # import ipdb;ipdb.set_trace()

    event = Event.objects.get(active=True, slug=event_slug) #event slug

    fund_obj = event.allowed_categories.filter(active=True).order_by('name').values('id','name','slug')
    
   
    cause_ids = event.ngo.values_list("cause_id",flat=True)
    cause_obj = Cause.objects.filter(id__in=cause_ids,active=True).order_by('name').values('id','name','slug')

    ngo_obj = event.ngo.filter(active=True,register_status=2).order_by('name').values('id','slug','name')
    
    ngo_cause_ids = NGO.objects.filter(active=True).values_list('cause__id',flat=True)

    select_cause = Cause.objects.filter(active=True,id__in=ngo_cause_ids).order_by('name')

    data=request.POST
    # slug = data.get('slug')
    slug = event_slug
    search = data.get('search')
    ngo = data.get('ngo')
    cause = data.get('cause')
    ftype_id = data.get('ftype')
    ftype_id = id
    event_obj = get_object_or_404(Event, slug=slug,active=True)
    data = [{"count": 0, "objlist": [], "pages": 0}]
    ftype_obj = FundraiserType.objects.get(id=ftype_id)
    
    # event_fundraisers = event_obj.fundraisers.filter(active=True, created_by__is_active=True)
    event_fundraisers = event_obj.fundraisers.filter(fundraiser_type=ftype_obj,active=True, created_by__is_active=True)

    search = request.GET.get("fundraiser_name")
    ngo = request.GET.get('ngo')
    cause = request.GET.get('cause')
    fundraiser_type = request.GET.get('fundraiser_type')

    
    if search and search !='null':
        if len(search) <= 2:
            event_fundraisers = event_fundraisers.filter(Q(created_by__first_name__istartswith=search) | Q(created_by__last_name__istartswith=search))
        else:
            event_fundraisers = event_fundraisers.filter(Q(created_by__first_name__icontains=search) | Q(created_by__last_name__icontains=search))
    if ngo and ngo !='null':
        ngo_obj = NGO.objects.get(id=ngo)
        event_fundraisers = event_fundraisers.filter(ngo=ngo_obj)
    if cause and cause !='null':
        cause_obj = Cause.objects.get(id=cause)
        event_fundraisers = event_fundraisers.filter(ngo__cause=cause_obj)
    badge = get_champion_badge(ftype_obj)
    fundraiser_list = []

    # for obj in event_fundraisers:

    #     try:
    #         if obj.icon.file:
    #             image = str(PHOTO_URL +obj.icon.url)     
    #     except:
    #         try:
    #             if obj.ngo.icon.file:
    #                 image = str(PHOTO_URL +obj.ngo.icon.url)
    #         except:
    #             image = PHOTO_URL +"/static/frontend/img/no-image.jpg"

        # fundraiser_list.append({"donation_count":int(obj.get_donation_count()),"goal_amount":obj.goal_amount,
        #                         "icon":image,
        #                         "name":obj.created_by.first_name + ' ' + obj.created_by.last_name,"slug":obj.slug,"id":obj.id,
        #                         "badge":badge,'pages':ceil(float(len(event_fundraisers)) / float(pg_size)) if event_fundraisers else 0,
        #                         "total_donations":int(obj.total_amount()),"donation_percentage":int(obj.percentage_donated()),
        #                         "key":"fundraiser","ngo_name":obj.ngo.name,"title_slug":obj.created_by.first_name.replace(' ','_')+'_'+obj.created_by.last_name.replace(' ','_')  ,
        #                         "ngo_slug":obj.ngo.slug,"share_description":strip_tags(obj.ngo.our_mission)})

    # paginator = CustomPagination()
    # result_page = paginator.paginate_queryset( fundraiser_list, request)
    # data = paginator.get_paginated_response(result_page,link)
    
    return render(request,'frontend_templates/fundraisertype_listing.html', locals())

