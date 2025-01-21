
from django import template
from django.utils.translation import activate
from Events.models import *

register = template.Library()

@register.simple_tag
def get_all_event_menus():
    # filtering active menus
    # for getting the all events which is in required field 
    return Event.objects.filter(event_type="Marathon", end_date__gte=datetime.today() ,active=True).exclude(slug="mysurumarathon")

@register.simple_tag
def get_all_campaign():
    # filtering the the all campaign 
    return Event.objects.filter(event_type='Campaign',active=True).exclude(slug='Water-Life')

@register.simple_tag
def our_program_event():
    # filtered the order by 
    return Event.objects.filter(active=True,event_type="Marathon").order_by('main_page_date')    
         

@register.simple_tag
def our_program_campaign_list():
    #filtered the Campaign list
    #this will give all campaing which don't have lenovocares slug
    return Event.objects.filter(event_type='Campaign',active=True).exclude(slug='lenovocares')
    
@register.filter
def get_article_menus():
    return Article.objects.filter(section__active=True,active=True).order_by("-created_on")[0:2]
    # return Article.objects.get(slug=slug,active=True)
  
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
    t120  = list(FundraiserType.objects.filter(name__icontains="120").values_list("name",flat=True))
    t220  = list(FundraiserType.objects.filter(name__icontains="220").values_list("name",flat=True))
    t160  = list(FundraiserType.objects.filter(name__icontains="160").values_list("name",flat=True))
    
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

@register.simple_tag
def eventfooter():
    # this function will work for getting the all event in footer section
    return  Event.objects.filter(active=True,feature_event=True).order_by('-id')

@register.simple_tag
def campaignfooter():
    return Event.objects.filter(active=True,end_date__gte=datetime.today(),event_type='Campaign').order_by('id')
            

