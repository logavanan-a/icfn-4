#!/usr/bin/python
# -*- coding: utf-8 -*-
# """
#This file contains user defined template tags to used templates to render values
# """

from mcms.models import *
from django import template
from django.http import HttpResponse
from csr.models import *
from NGO.models import *
from mcms.models import *
from Events.models import *
from django.db.models import Q, Sum
from datetime import date, datetime
import itertools
import os
from membership.models import *
from wishtree.models import *

register = template.Library()

import random
#--------------------
@register.filter
def shuffle(arg):
    # function shuffle
    # this function takes arg as a parameter
    # Returns a random item from the given list.
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp

@register.filter
def get_event_types():
    # function get event types
    # return all the eventtypes
    etypes = Event_Type.objects.all()
    return etypes

@register.filter
def get_ngo_indvidual_user(request):
    # function ngo individual user
    # return whether the user is a 
    # NGO
    # CSR
    # INDIVIDUAL
    # if neither of the above 
    # empty string will be passed
    check = ''
    ngo_user = ''
    csr_user = ''
    usr = request.user.pk
    try:
        ngo_user = NGO.objects.filter(contact_person__user__pk = usr)
        csr_user = CSR.objects.filter(contact_person__user__pk = usr)
        if ngo_user:
            check = 'NGO'
        elif csr_user:
            check = 'CSR'
        elif usr:
            check = 'INDIVIDUAL'
    except:
        pass
    return check

@register.filter
def get_events(request):
    # function get events
    # returns a list of events 
    # that are active
    # future_event_list list all the events that are not completed
    # prev_event_list lists all the events that are completed
    future_event_list = Event.objects.filter(active=True, main_page_date__gte=datetime.today()).order_by('main_page_date')
    prev_event_list = Event.objects.filter(active=True, main_page_date__lt=datetime.today()).order_by('-main_page_date')
    result = list()
    event_list = itertools.chain(future_event_list, prev_event_list)
    map(lambda x: not x in result and result.append(x), event_list)
    return result

@register.filter
def get_events_enddate(request):
    # function get events
    # returns a list of events 
    # that are active
    # future_event_list list all the events that are not completed
    # prev_event_list lists all the events that are completed main_page_date__gte=datetime.today(),
    future_event_list = Event.objects.filter(active=True, end_date__gte=datetime.today()).order_by('main_page_date')
    result = list()
    event_list = itertools.chain(future_event_list)
    map(lambda x: not x in result and result.append(x), event_list)
    return result

@register.filter
def get_giving_menus(request):
    # function giving menus
    # return all the articles related to
    # section giving
    # if section none
    # empty string will be passed
    section = ''
    articles = ''
    section = Section.objects.get_or_none(name='giving', active=True)
    if section:
        articles = Article.objects.filter(section=section, active=True)
    return articles

@register.filter
def get_fundraising_menus(request):
    # function fundraising menus
    # return all the articles related to
    # section fundraising
    # if section none
    # empty string will be passed
    section = ''
    articles = ''
    section = Section.objects.get_or_none(name='fundraising', active=True)
    if section:
        articles = Article.objects.filter(section=section, active=True)
    return articles

@register.filter
def get_events_menus(request):
    # function events menus
    # return all the articles related to
    # section events
    # if section none
    # empty string will be passed
    section = ''
    articles = ''
    section = Section.objects.get_or_none(name='events', active=True)
    if section:
        articles = Article.objects.filter(section=section, active=True)
    return articles

@register.filter
def get_community_menus(request):
    # function community menus
    # return all the articles related to
    # section community
    # if section none
    # empty string will be passed
    section = ''
    articles = ''
    section = Section.objects.get_or_none(name='community', active=True)
    if section:
        articles = Article.objects.filter(section=section, active=True)
    return articles

@register.filter
def get_mainpage_menus(request):
    # function mainpage menus
    # return all the articles related to
    # section main-home-page
    # if section none
    # empty string will be passed
    section = ''
    articles = ''
    section = Section.objects.get_or_none(name="Main-home-page", active=True)
    if section:
        articles = Article.objects.filter(section=section, active=True).order_by('?')[:1]
    return articles

@register.filter
def get_event_article(request, eid=''):
    # function event article
    # request and eid are the parameter passed to the function
    # event
    # if event is present 
    # event related articles will be passed to the template
    # only the 3 articles will be passed
    # this function is used in the home page of event
    event = ''
    event = Event.objects.get_or_none(id=eid)
    if event:
        articles = EventArticle.objects.filter(content_type=ContentType.objects.get(model__iexact = 'event'), object_id=event.id, display=1).order_by('?')[:3]
    return articles

@register.filter
def get_display_fundraisers(request, eid):
    # function get event fundraisers
    # request and eid are the parameter passed to the function
    # event
    # if event is present 
    # event related fundraisers will be passed to the template
    # only the fundraisers with the category 
    # that are tagged for the event 
    # will be passed to the templates
    event = ''
    flist =[]
    event = Event.objects.get_or_none(id=eid)
    if event:
        ftype = event.display.filter(active=True)
        for i in ftype:
            f = event.fundraisers.filter(fundraiser_type = i, active=True, created_by__is_active=True)
            for j in f:
                flist.append(j)
    return flist

@register.filter
def get_ftype_fundraisers(eid, ftype_id):
    # function get ftype fundraisers
    # ftype_id and eid are the parameter passed to the function
    # event
    # if event is present 
    # event related fundraisers will be passed to the template
    # only the fundraisers with the category ftype
    # will be passed to the templates
    event = ''
    ftype = ''
    flist = []
    fcount = 00
    ncount = 00
    event = Event.objects.get_or_none(id=eid)
    ftype = FundraiserType.objects.get_or_none(id=ftype_id)
    t10s = list(FundraiserType.objects.filter(name__icontains="10").values_list("name",flat=True))
    t15s = list(FundraiserType.objects.filter(name__icontains="15").values_list("name",flat=True))
    t25s = list(FundraiserType.objects.filter(name__icontains="25").values_list("name",flat=True))
    t30s = list(FundraiserType.objects.filter(name__icontains="30").values_list("name",flat=True))
    t40s = list(FundraiserType.objects.filter(name__icontains="40").values_list("name",flat=True))
    t45s = list(FundraiserType.objects.filter(name__icontains="45").values_list("name",flat=True))
    t12s = list(FundraiserType.objects.filter(name__icontains="12").values_list("name",flat=True))
    t60s = list(FundraiserType.objects.filter(name__icontains="60").values_list("name",flat=True))
    t100s = list(FundraiserType.objects.filter(name__icontains="100").values_list("name",flat=True))
    t7s   = list(FundraiserType.objects.filter(name__icontains="7").values_list("name",flat=True))
    t120   = list(FundraiserType.objects.filter(name__icontains="120").values_list("name",flat=True))
    t220   = list(FundraiserType.objects.filter(name__icontains="220").values_list("name",flat=True))
    t160   = list(FundraiserType.objects.filter(name__icontains="160").values_list("name",flat=True))
    
    if event:
        team10s = DuplicateCorporates.objects.filter(active = True, team__in = t10s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team15s = DuplicateCorporates.objects.filter(active = True, team__in = t15s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team25s = DuplicateCorporates.objects.filter(active = True, team__in = t25s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team30s = DuplicateCorporates.objects.filter(active = True, team__in = t30s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team40s = DuplicateCorporates.objects.filter(active = True, team__in = t40s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team45s = DuplicateCorporates.objects.filter(active = True, team__in = t45s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team12s = DuplicateCorporates.objects.filter(active = True, team__in = t12s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team60s = DuplicateCorporates.objects.filter(active = True, team__in = t60s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team100s = DuplicateCorporates.objects.filter(active = True, team__in = t100s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team7s = DuplicateCorporates.objects.filter(active = True, team__in = t7s, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team120s = DuplicateCorporates.objects.filter(active = True, team__in = t120, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team220s = DuplicateCorporates.objects.filter(active = True, team__in = t220, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']
        team160s = DuplicateCorporates.objects.filter(active = True, team__in = t160, event=event).aggregate(Sum('no_of_teams'))['no_of_teams__sum']

    try:
        if ftype:
            print(ftype.name)
            ncount = "%02d"%(event.fundraisers.filter(fundraiser_type=ftype, active=True, created_by__is_active=True).count())
            if team10s is None:
                team10s = 00
            elif team25s is None:
                team25s = 00
            elif team30s is None:
                team30s = 00
            elif team40s is None:
                team40s = 00
            elif team12s is None:
                team12s = 00
            elif team60s is None:
                team60s = 00
            elif team7s is None:
                team7s  = 00
            elif team120s is None:
                team120s = 00
            elif team220s is None:
                team220s = 00
            elif team160s is None:
                team160s = 00

            if ncount is None:
                ncount = 00
            if ftype.name in t10s:
                fcount = "%02d"%(int(ncount) + int(team10s))
            elif ftype.name in t15s:
                fcount = "%02d"%(int(ncount) + int(team15s))
            elif ftype.name in t25s:
                fcount = "%02d"%(int(ncount) + int(team25s))
            elif ftype.name in t30s:
                fcount = "%02d"%(int(ncount) + int(team30s))
            elif ftype.name in t40s:
                fcount = "%02d"%(int(ncount) + int(team40s))
            elif ftype.name in t45s:
                fcount = "%02d"%(int(ncount) + int(team45s))
            elif ftype.name in t12s:
                fcount = "%02d"%(int(ncount) + int(team12s))
            elif ftype.name in t60s:
                fcount = "%02d"%(int(ncount) + int(team60s))
            elif ftype.name in t100s:
                fcount = "%02d"%(int(ncount) + int(team100s))
            elif ftype.name in t7s:
                fcount = "%02d"%(int(ncount) + int(team7s))
            elif ftype.name in t120:
                fcount = "%02d"%(int(ncount) + int(team120s))
            elif ftype.name in t220:
                fcount = "%02d"%(int(ncount) + int(team220s))
            elif ftype.name in t160:
                fcount = "%02d"%(int(ncount) + int(team160s))
            else:
                fcount = ncount
    except:
        pass
    return fcount

@register.filter
def get_scroller_fundraisers(request, eid):
    # function get scroller fundraisers
    # request and eid are the parameter passed to the function
    # event
    # if event is present 
    # event related fundraiser will be passed to the template
    # only the fundraisers with the category 
    # that are tagged for the event 
    # will be passed to the templates
    event = ''
    flist =[]
    event = Event.objects.get_or_none(id=eid)
    if event:
        ftype = event.display_one.filter(active=True)
        for i in ftype:
            if i.name.startswith('Corporate Cares'): #Checking to display only Corporate cares
                f = event.fundraisers.filter(fundraiser_type = i, active=True)
                for j in f:
                    flist.append(j)
    return flist

@register.filter
def is_corporate(ftypeid, eid):
    # function is corporate
    # checks whether the fundraiser is an corporate or not
    # return true
    # if fundraiser is a corporate
    # else
    # return false
    # if fundraiser is not a corporate
    status = False
    event = ''
    flist =[]
    ftype=''
    event = Event.objects.get_or_none(id=eid)
    ftype = FundraiserType.objects.get_or_none(id=ftypeid)
    if event and ftype:
        flist = event.display_one.filter(active=True)
        if ftype in flist:
#            #status = True
            status = False
    return status

@register.filter
def get_fundraiser(request, fid):
    # function get fundraiser
    # request and fid are the parameter passed to the function
    # fid specifies the id of the fundraiser
    # it checks whether the fundraiser is there or not
    # if fundraiser exists
    # returns true
    # else
    # return false
    check = False
    usr = request.user
    try:
        if usr:
            f_obj = Fundraiser.objects.filter(created_by=usr, id=fid)
            if f_obj:
                check = True
            return check
    except:
        check = False
        return check

@register.filter
def get_ngo(request, nid):
    # function get ngo
    # request and nid are the parameter passed to the function
    # nid specifies the id of the fundraiser
    # it checks whether the ngo is there or not
    # if ngo exists
    # returns true
    # else
    # return false
    check = False
    usr = request.user
    try:
        if usr:
            ngo_obj = NGO.objects.filter(contact_person__user=usr, id=nid)
            if ngo_obj:
                check = True
            return check
    except:
        check = False
        return check

@register.filter
def get_ngoevents(request, ngo_id):
    # function get ngo events
    # request, ngo_id are the parameters passed to the event
    # this function is used to return 
    # all the ngos related to the event
    # this function is used in main ngo listing page
    event_list = Event.objects.filter(Q(event_type = "Marathon") | Q(event_type = "Daan Utsav")| Q(event_type = "Cyclothon"))
    event_lists = []
    for event in event_list:
        if event.ngo.filter(id=ngo_id):
            event_lists.append(event)
    return event_lists

@register.filter
def is_in_event(request, ngid):
    # function is in event
    # request, ngid are the parameters passed to the event
    # this function is used to check whether the 
    # ngo is participated in the event or not
    key = "general"
    events = Event.objects.filter(active=True)
    ngo = NGO.objects.get(id=ngid)
    for event in events:
        if ngo in event.ngo.all():
            return event.slug
    return key

import locale
#locale.setlocale(locale.LC_ALL, 'en_IN')

@register.filter
def getnumber(val):
    return locale.format("%d", int(val), grouping=True)

@register.simple_tag
def can_donate(ngo, event):
    # function can donate
    # ngo event are the parameters passed to the event
    # this function checks
    # wheather ngo can accept donation
    # wheather event can accept donation
    # if any of the event or ngo does not
    # accept_donation is donation is false
    # event or ngo will not be able to accept donation
    check = any([ngo and not event and ngo.accept_donation, all([ngo, event, event.accept_donation, ngo.accept_donation]), event and not ngo and event.accept_donation])
    return check

@register.simple_tag
def check_ngo_in_event(ngo, event):
    # function check ngo in event
    # ngo event are the parameters passed to the event
    # this function checks
    # whether an ngo is participated in event
    # return true
    # if ngo participated
    # else
    # return false
    # if not participated
    check = False
    event_obj = Event.objects.get(id=int(event))
    if event_obj.ngo.filter(id=int(ngo)):
        check = True
    return check
    
def get_templateevent_ngo_online_donations(eid, ngoid):
    amt = 0
    d= Donation.objects.filter(event__id= eid, ngo__id=ngoid, payment_status= "Success")
    for i in d:
        amt = amt + i.amount
    return amt

def get_templateevent_ngo_offline_donations(eid, ngoid):
    amt = 0
    d= OfflineDonation.objects.filter(event__id= eid, ngo__id=ngoid)
    for i in d:
        amt = amt + i.amount
    return amt


@register.simple_tag
def count_ngo_event_donation(ngo,event):
    olamount = get_templateevent_ngo_online_donations(event,ngo)
    offamount = get_templateevent_ngo_offline_donations(event, ngo)
    return olamount , offamount


@register.simple_tag
def check_fundraiser_in_event(fund, event):
    status = False
    event_obj = Event.objects.get(id=int(event))
    donations = Donation.objects.filter(event=event_obj, payment_status="Success")
    if event_obj.fundraisers.filter(id=int(fund)):
        fund_list = []
        fund_list.append(int(fund))
        check = donations.filter(fundraiser__id__in = fund_list)
        check1 = OfflineDonation.objects.filter(fundraiser__id__in=fund_list, event=event_obj)
        if check or check1:
            status = True
    return status

@register.filter
def get_home_fundraisers(request, eid):
    event = ''
    flist =[]
    event = Event.objects.get_or_none(id=eid)
    if event:
        flist = event.fundraisers.filter(active=True, created_by__is_active=True).order_by('?')[:12]
    return flist


@register.filter
def is_past_due(self):
    status = False
    if date.today() > self.end_date:
        status = True
    return status

@register.filter
def get_event_started(request, eid):
    event = ''
    status = False
    event = Event.objects.get_or_none(id=eid)
    if event.start_date <= datetime.today().date():
        status = True
    return status

@register.filter
def get_amount_deduction(request):
    ded = 2
    try:
        ded_obj = EventAmountDeduction.objects.get(Q(start_date__lte=datetime.today().date())&Q(end_date__gte=datetime.today().date()), event=None, etype='Wishtree')
        ded = float(ded_obj.percent)
        if ded.is_integer():
            ded = int(ded)
    except:
        pass
    return ded


@register.filter
def get_fundraiserevents(request, fund_id):
    event_list = Event.objects.filter(Q(event_type = "Marathon") | Q(event_type = "Cyclothon"))
    event_lists = []
    for event in event_list:
        if event.fundraisers.filter(id=fund_id):
            event_lists.append(event)
    return event_lists


@register.filter
def get_latest_blogs(request):
    blog_list = Blog.objects.filter(active=True).order_by('-id')[:2]
    return blog_list


@register.filter
def get_dict(request):
    #create a dict with the years and months:blogs 
    blog_list = Blog.objects.filter(active=True).order_by('-blog_date')
    w_dict = {}
    for i in range(blog_list[0].blog_date.year, blog_list[len(blog_list)-1].blog_date.year-1, -1):
        w_dict[i] = {}
        for month in range(1,13):
            w_dict[i][month] = []
    for blog in blog_list:
        w_dict[blog.blog_date.year][blog.blog_date.month].append(blog)
    #this is necessary for the years to be sorted
    w_sorted_keys = list(reversed(sorted(w_dict.keys())))
    list_wfs = []
    for key in w_sorted_keys:
        adict = {key:w_dict[key]}
        list_wfs.append(adict)
    return list_wfs

@register.filter
def get_blog_count(request, year):
    blog_list = Blog.objects.filter(active=True, blog_date__year=year).count()
    return blog_list


@register.filter
def get_tag_clouds(request):
    return Tags.objects.filter(active=True)


@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter
def filename(value):
    return os.path.basename(value.file.name)

@register.simple_tag
def get_latest_annual_report():
    section = Section.objects.get(slug='about-us')
    attachment = section.get_section_atachment().filter().latest('id')
    return attachment

@register.simple_tag
def get_csr_project_permision(request):
    status, csruser = False, None
    user = request.user
    try:
        csruser = CsrUsers.objects.get_or_none(user=user, subscribed=True)
    except:
        pass
    if csruser or user.is_superuser:
        status = True
    return status

@register.simple_tag
def divide(value, arg):
    return value/arg

@register.simple_tag
def get_latest_event(request):
    event = None
    try:
        event = Event.objects.filter(event_type="Marathon", active=True).exclude(slug="mysurumarathon").latest('id')
    except:
        pass
    return event

@register.simple_tag
def get_count_user(request):
    contents = HomePageContent.objects.filter(active=True)
    fundraiser = sum([int(i.fundraisers) for i in contents if i.fundraisers])
    donation = sum([int(i.donors) for i in contents if i.donors])
    our_reach = sum([int(i.our_reach) for i in contents if i.our_reach])
    amount_raised = sum([int(i.amount_raised) for i in contents if i.amount_raised])
    beneficiaries = sum([int(i.beneficiaries) for i in contents if i.beneficiaries])
    visitors = sum([int(i.visitors) for i in contents if i.visitors])
    d = {'fundraiser':fundraiser, 'donation':donation, 'amount_raised':amount_raised, 'our_reach':our_reach, 'beneficiaries':beneficiaries, 'visitors':visitors}
    return d

@register.simple_tag
def get_event_fundraiser_amount(request, fund_obj, event_obj):
    
    amt=0.,
    offamt = 0
    latest_offline_donated = None
    latest_online_donated = None
    d = Donation.objects.filter(fundraiser=fund_obj, payment_status='Success', event=event_obj).filter(event__active=True)
    d1 = OfflineDonation.objects.filter(fundraiser=fund_obj, event=event_obj).filter(event__active=True)
    for i in d:
        amt = amt + i.amount
    for offd in d1:
        offamt = offamt + offd.amount
    tot_amt = amt + offamt
    try:
        donated = float(tot_amt) * 100 / float(fund_obj.goal_amount)
    except:
        donated = 0
    donationcount = d.count() + d1.count()
    try:
        latest_offline_donated = OfflineDonation.objects.filter(fundraiser=fund_obj, event=event_obj).filter(event__active=True).latest('id')
    except:
        pass
    try:
        latest_online_donated = Donation.objects.filter(fundraiser = fund_obj, payment_status='Success', event=event_obj).filter(event__active=True).latest('id')
    except:
        pass
    d = {'donated':int(donated), 'tot_amt':tot_amt, 'donationcount':donationcount, 'latest_online_donated':latest_online_donated, 'latest_offline_donated':latest_offline_donated}
    return d

@register.filter
def get_events_joinus(request):
    # function get events
    # returns a list of events 
    # that are active
    # future_event_list list all the events that are not completed
    # prev_event_list lists all the events that are completed
    future_event_list = Event.objects.filter(display_in_joinus=True, active=True, end_date__gte=datetime.today())
    result = list()
    event_list = itertools.chain(future_event_list)
    map(lambda x: not x in result and result.append(x), event_list)
    return result

@register.simple_tag
def get_page_banners(request, key='', event_obj=None):
    if key == '' and not event_obj:
        banner_obj = PageBanners.objects.filter(ptype='others').order_by('?')[0]
    elif event_obj and PageBanners.objects.filter(event=event_obj) and not key == 'thankyou':
        banner_obj = PageBanners.objects.filter(event=event_obj).order_by('?')[0]
    elif not key == '':
        banner_obj = PageBanners.objects.filter(ptype=key).order_by('?')[0]
    else:
        banner_obj = PageBanners.objects.filter(ptype='others').order_by('?')[0]
    return banner_obj

@register.simple_tag
def get_search_ngo(request, slug='', event=''):
    events = []
    active_event = ''
    if not slug == '':
        try:
            ngo = NGO.objects.get(slug=slug)
            events = max([int(i.id) for i in get_ngoevents(request, int(ngo.id))])
            active_event = Event.objects.get(id=int(events))
        except:
            pass
    if not event == '':
        active_event = Event.objects.get(slug=event,active=True)
    return active_event

@register.simple_tag
def get_search_fundraiser(request, slug='', event=''):
    events = []
    active_event = ''
    if not slug == '':
        try:
            fund = Fundraiser.objects.get(slug=slug)
            events = max([int(i.id) for i in get_fundraiserevents(request, int(fund.id))])
            active_event = Event.objects.get(id=int(events))
        except:
            pass
    if not event == '':
        active_event = Event.objects.get(slug=event,active=True)
    return active_event

@register.simple_tag
def get_members(request):
    return Members.objects.filter(active=True)

@register.simple_tag
def get_event_donation_amount(request, event_obj):
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

@register.simple_tag
def get_active_events(request):
    event_type = ['Marathon']
    return Event.objects.filter(active=True, accept_donation=True, event_type__in=event_type).exclude(slug="edudaan")

@register.simple_tag
def get_event_wishtree(request):
    return WishTree.objects.filter(active=True, is_main_page=True, event__accept_donation=True).exclude(event=None)

@register.simple_tag
def get_joinable_events(request):
    return Event.objects.filter(active=True, accept_donation=True, event_type="Marathon")

@register.simple_tag
def get_userjoinable_events(request, cso):
    user = request.user
    event_list = [i for i in Event.objects.filter(active=True, accept_donation=True, event_type="Marathon") if not cso in i.ngo.all() if not CSORequestToParticipate.objects.filter(cso=cso, event=i)]
    return event_list

@register.simple_tag
def get_csouser_events(request, cso):
    user = request.user
    csouser = CSOUsers.objects.filter(cso=cso, user=user)
    if csouser:
        event_list = [i for i in Event.objects.filter(active=True, accept_donation=True, event_type="Marathon") if cso in i.ngo.all() if CSORequestToParticipate.objects.filter(cso=cso, event=i, user=user, is_joined=True)]
    else:
        event_list = []
        event_list1 = [event_list.append(i) for i in Event.objects.filter(active=True, accept_donation=True, event_type="Marathon") if cso in i.ngo.all() if not CSORequestToParticipate.objects.filter(cso=cso, event=i, is_joined=True)]
        event_list2 = [event_list.append(i) for i in Event.objects.filter(active=True, accept_donation=True, event_type="Marathon") if cso in i.ngo.all() if CSORequestToParticipate.objects.filter(cso=cso, event=i, user=user, is_joined=True)]
        event_list = list(set(event_list))
    return event_list
