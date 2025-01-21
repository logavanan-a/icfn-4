from django.db import models
from NGO.models import *
from mcms.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from mcms.thumbs import ImageWithThumbsField
from datetime import timedelta, datetime
from django.db.models import Q
from wishtree.models import *
from csr.views import *

# EVENT_CHOICES will be used to presenting a event page for the users
# following are the event types
# Marathon
# Daan Utsav
# Cyclothon
# Campaign
# Others
EVENT_CHOICES = ( (u'Marathon', u'Marathon'), (u'Daan Utsav', u'Daan Utsav'), (u'Cyclothon', u'Cyclothon'), (u'Campaign', u'Campaign'), (u'Others', u'Others'))
DISPLAY_CHOICES = ( (u'1', u'Home Page'),)
CAMPAIGN_CHOICES =  ( (u'GC', u'Genral Campaign'), (u'CFC', u'Campaign with CSO and Fundraiser'), (u'FC', u'Campaign with isupport fundraisers'))
class EventBanners(Base):
    # module event banners
    # this module stores all the event banners
    # used to display banners on the
    # event home page
    # content_type and object_id are the default field 
    # names GenericForeignKey will look for.
    name = models.CharField(max_length=100)
    image = ImageWithThumbsField(upload_to='static/%Y/%m/%d', sizes=((90,120),(120,120),(180,240),(360,480),(480,720),(340,900),(900,300),(980,300)),blank=True,null=True,help_text="Image size should be 930x300 pixels")
    caption = models.CharField("Caption", blank=True, null=True, max_length=50)
    description = models.CharField("Description", blank=True, null=True, max_length=300)
    URL = models.URLField("Link url", max_length=200, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')
    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return '%s'%(self.name)

class EventArticle(Base):
    # module event article
    # this module stores all the event article
    # used to display article on the
    # event article page
    # content_type and object_id are the default field 
    # names GenericForeignKey will look for.
    name = models.CharField(max_length=100)
    display = models.CharField("Display", blank=True, null=True, max_length=400,choices=DISPLAY_CHOICES)
    summary = models.CharField("Byline/ Summary", blank=True, null=True, max_length=2000)
    description = RichTextField(blank=True, null=True)
    image = ImageWithThumbsField(upload_to='static/%Y/%m/%d', sizes=((90,120),(92,114),(120,120),(180,240),(360,480),(480,720),(340,900),(900,300),(980,300)),blank=True,null=True,help_text="Image size should be 930x300 pixels",validators=[validate_image])
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen", max_length=60)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')
    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return u'%s'%(self.name)

class AllowedCategory(Base):
    # module allowed category
    # this module stores all the categories that are allowed for the event
    # A slug field in Django is used to store 
    # and generate valid URLs for your dynamically created web pages.
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField("Slug")


    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return u'%s'%(self.name)


class ContributingHotels(Base):
    # module contributing hotels
    # this module stores all the hotels of the event
    # A slug field in Django is used to store 
    # and generate valid URLs for your dynamically created web pages.
    name = models.CharField(blank=True, null=True, max_length=100)
    image = models.ImageField('Icon', upload_to='static/%Y/%m/%d', blank=True, null=True ,validators=[validate_image])
    url = models.URLField(blank=True, null=True, max_length=100)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen", max_length=60)


    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return u'%s'%(self.name)

    class Meta:
         db_table = 'Events_contributing_hotels'

class CorporateTables(Base):
    # module corporate tables
    # this module stores all the corporate tables of the event
    # A slug field in Django is used to store 
    # and generate valid URLs for your dynamically created web pages.
    name = models.CharField(blank=True, null=True, max_length=100)
    image = models.ImageField('Icon', upload_to='static/%Y/%m/%d', blank=True, null=True,validators=[validate_image] )
    url = models.URLField(blank=True, null=True, max_length=100)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen", max_length=60)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return u'%s'%(self.name)

    class Meta:
         db_table = 'Events_corporate_tables'

class Event(Base):
    # module event
    # this module stores all the events
    # A slug field in Django is used to store 
    # and generate valid URLs for your dynamically created web pages.
    # small_image field is used in main page 
    # display field is used to display fundraiser type in event home page
    # display_one field is used to display fundraiser type in scoller 
    # of event home page
    # color field specifies the color of the event
    # main_page_logo field is used to show event logo in the main page
    # main_page_date field is used to show event date in the main page
    # accept_donation field is used for allowing the user to donate in the event
    # if accept_donation is false donation should not be done in the event
    # if accept_donation is true event should accept donation
    event_type = models.CharField("Event Type", blank=True, null=True, max_length=400,choices=EVENT_CHOICES)
    campaign_type = models.CharField("Campaign Type", blank=True, null=True, max_length=400,choices=CAMPAIGN_CHOICES)
    name = models.CharField('Event Name',max_length=100)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField("Event URL/Slug")
    allowed_categories = models.ManyToManyField(FundraiserType, related_name='Select Fundariser/Team Categories applicable for event+')
    start_date = models.DateField('Event Start Date',blank=True, null=True)
    # end_date = models.DateField('ent End Date',blank=True, null=True)
    end_date = models.DateField('Event End Date',blank=True, null=True)
    widget = ImageWithThumbsField('Icon', upload_to='static/%Y/%m/%d', sizes=((90,120),(92,114),(100,74), (626,372),(626,250),(214,127)),blank=True,null=True,validators=[validate_image])
    widget_icon = ImageWithThumbsField('Event Widget', upload_to='static/%Y/%m/%d', sizes=((200, 200), (90, 120), (180, 240)), blank=True, null=True,validators=[validate_image])
    ngo = models.ManyToManyField(NGO)
    fundraisers = models.ManyToManyField(Fundraiser)
    accept_donation = models.BooleanField(default=True)
    allow_fundraisers = models.BooleanField(default=False)
    color = models.CharField(blank=True, null=True, max_length=100)
    wishtree_color = models.CharField(blank=True, null=True, max_length=100)
    wishtree_logo = ImageWithThumbsField('Wishtree logo', upload_to='static/%Y/%m/%d', sizes=((90,120),(170,101)),blank=True,null=True,validators=[validate_image])
    wishtree_classname = models.CharField(blank=True, null=True, max_length=100)
    display = models.ManyToManyField(FundraiserType, related_name='fundraisertype_related_to_event')
    display_name = models.CharField('Name', max_length=100, blank=True, null=True)
    display_one = models.ManyToManyField(FundraiserType, related_name='fundraisertype_related_to_event_for_frontend_scroller')
    display_one_name = models.CharField('Name', max_length=100, blank=True, null=True)
    contributing_hotels = models.ManyToManyField(ContributingHotels)
    corporate_tables = models.ManyToManyField(CorporateTables)
    summary = models.TextField(blank=True, null=True)
    small_image = ImageWithThumbsField('Small Image', upload_to='static/%Y/%m/%d', sizes=((90,120),(10,10),(20,30)),blank=True,null=True,validators=[validate_image])
    main_page_logo = ImageWithThumbsField('Event Archive Logo', upload_to='static/%Y/%m/%d', sizes=((180, 120), (140, 90), (90, 140)), blank=True, null=True,validators=[validate_image])
    main_page_date = models.CharField('Event Date', max_length=100, blank=True, null=True)
    listing_order = models.IntegerField(default=1)
    meta_title = models.CharField("Meta Page Title", max_length=200, blank = True, null=True)
    meta_description = models.TextField("Meta Description", blank = True, null=True)
    event_email = models.EmailField("Event Contact Email ID", blank=True, null=True, max_length=100)
    join_us_logo = ImageWithThumbsField('Event logo', upload_to='static/%Y/%m/%d', sizes=((90,120),(111,40)),blank=True,null=True,validators=[validate_image])
    display_in_joinus = models.BooleanField(default=False)
    feature_event     = models.BooleanField(default=False)
    home_page_widget = ImageWithThumbsField('Home Page Logo', upload_to='static/%Y/%m/%d', sizes=((292, 95), (90, 140)), blank=True, null=True,validators=[validate_image])
    external_url = models.CharField('External URL', max_length=100, blank=True, null=True)
    target = models.CharField('Target amount', max_length=100, blank=True, null=True)
    fundraiser_donation = models.BooleanField(default=False)
    fundraiser_donation_amount = models.CharField('Fundraiser Donation Amount', max_length=100, blank=True, null=True)
    banner_title              = models.CharField("Add a Banner header",max_length=200,blank=True,null=True)
    banner_image              = ImageWithThumbsField('Home page Banner', upload_to='static/banner/%Y/%m/%d',blank=True,null=True)
 

    def __str__(self):
        return self.name

    def get_wishtree(self):
        return WishTree.objects.filter(event=self)

    def get_images(self):
        return EventBanners.objects.filter(content_type__model__iexact="event", object_id=self.id, active=True)

    def get_vedios(self):
        return Link.objects.filter(active=True,content_type__model__iexact="event", object_id=self.id)

    def get_videos_for_event(self):
        return Link.objects.filter(content_type__model__iexact="event", object_id=self.id).order_by('?')[:1]

    def get_closing_date(self):
        closing_date = self.end_date+timedelta(days=20)
        return closing_date

    def get_amount_deduction(self):
        try:
            ded_obj = EventAmountDeduction.objects.get(Q(start_date__lte=datetime.today().date())&Q(end_date__gte=datetime.today().date()), event=self)
            return ded_obj.percent
        except:
            return 5

    def get_awards(self):
        try:
            return EventAwards.objects.get(event=self)
        except:
            return None

    def get_runreport(self):
        try:
            return EventRunReport.objects.get(event=self)
        except:
            return None

    def get_successstories(self):
        try:
            return EventSuccessStoreis.objects.get(event=self)
        except:
            return None

    def get_active_fundraisers(self):
        try:
            return self.fundraisers.filter(active=True, created_by__is_active=True)
        except:
            pass

    def get_event_dockets_annaul_reports(self):
        return AnnualReport.objects.filter(event=self,active=True,filetype='Docket')

    def is_eventdone(self):
        from datetime import datetime
        today = datetime.today().date()
        if today>self.end_date:
            return True
        else:
            return False
    def display_fundraisercreationpage(self):
        #for campaing having type as General Category create fundraiser wont come in the dropdown
        if self.event_type == "Campaign":
            if self.campaign_type == "GC":
                data = False
                return data
        # import ipdb;ipdb.set_trace()
        eventclose = self.is_eventdone()
        accept_donation = self.accept_donation
        if accept_donation == True and eventclose == False:
            data = True
        # elif accept_donation == True and eventclose == True:
        #     data = False
        # elif accept_donation == False and eventclose == True:
        #     data = False
        else:
            data = False
        return data


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



class EventAboutUs(Base):
    # module event about us
    # this module stores all the event details
    # event_link specifies the link of the event
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True)
    event_link = models.URLField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.event.name

EventDonationChoice = (('Other', 'Other'), ('Wishtree', 'Wishtree'))
class EventAmountDeduction(Base):
    # module event amount deduction
    # this module stores all the event amount deduction percent
    # start_date specifies start date of event amount deduction
    # end_date specifies end date of event amount deduction
    # percent specifies the percentage of amount 
    # to be detected from the event
    etype = models.CharField(max_length=100, choices=EventDonationChoice, blank=True, null=True, default='Other')
    event = models.ForeignKey(Event, blank=True, null=True,on_delete=models.CASCADE)
    start_date = models.DateField('Start date',blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    percent = models.DecimalField(max_digits=10,decimal_places=1)
    def __str__(self):
        return u'%s-%s'%(self.event, self.percent)


class EventContactUs(Base):
    # module event contact us
    # this module stores all the event contact details
    # all the address of the event will be stored in this module
    # event phone numbers will be stored
    # event contact persons email will be stored
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True)
    latitude = models.CharField(blank=True, null=True, max_length=100)
    longitude = models.CharField(blank=True, null=True, max_length=100)
    phone1 = models.CharField(blank=True, null=True, max_length=100)
    phone2 = models.CharField(blank=True, null=True, max_length=100)
    email1 = models.EmailField('Email*', max_length=60)
    email2 = models.EmailField('Email*', max_length=60, blank=True, null=True)
    address1 = models.CharField(blank=True, null=True, max_length=100)
    address2 = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    pincode = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.event.name


class EventThankMsg(Base):
    # module event thank message
    # used to store the thanks message of the event
    # this is used when a donor donates to the event
    # a mail will be sent to the donor
    # in that mail this message will be displayed
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True)
    image = ImageWithThumbsField('Image', upload_to='static/%Y/%m/%d', sizes=((90, 120), (92, 114), (626, 372), (626, 250),(214, 127)), blank=True, null=True,validators=[validate_image])

    def __str__(self):
        return self.event.name


class EventNgoDescription(Base):
    # module event ngo description
    # used to store the ngo description of the event
    # this is used when an ngo need to 
    # participate in more than one event
    # this is used when a ngo need a description
    # that required for the particular event
    # ngo can have there own 
    # work_acheivement
    # Fund Utilisation statement
    # Mission Statement
    # Youtube Embedded Link
    # Black board messages
    # Web Address
    # Mobile
    # for the particular event
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGO,blank=True,null=True,on_delete=models.CASCADE)
    contact_person = models.CharField(blank=True, null=True, max_length=200)
    email = models.EmailField(blank=True, null=True)
    work_acheivement = RichTextField('Our Work', help_text="Should not exceed 2000 characters",blank=True, null=True)
    fund_utilisation_statement = models.CharField('Fund Utilisation statement', max_length=300, blank=True, null=True)
    our_mission = models.TextField('Mission Statement', blank=True, null=True)
    youtube_embedd = models.URLField('Youtube Embedded Link', blank=True, null=True)
    black_board_message = models.TextField('Black board messages', blank=True, null=True)
    web_address = models.URLField('Web Address', blank=True, null=True)
    phone1 = models.CharField('Phone1',max_length=15, blank=True, null=True)
    mobile = models.CharField('Mobile', max_length=100, blank=True, null=True)
    address1 = models.CharField('Address1', max_length = 500, blank=True, null=True)
    address2 = models.CharField('Address2', max_length = 500, blank=True, null=True)
    country = models.ForeignKey('mcms.Country', blank = True, null = True,on_delete=models.CASCADE)
    state = models.ForeignKey('mcms.State', blank = True, null = True,on_delete=models.CASCADE)
    city = models.CharField('City', max_length = 100, blank=True, null=True)
    pincode = models.CharField('Pincode', max_length = 100, blank=True, null=True)

    def __str__(self):
        return u'%s-%s'%(self.event, self.ngo)


class EventAwards(Base):
    # module event awards
    # this module is used to store the event awards
    # this is used in the event about us page
    # where user can see the all the
    # awards of events
    # A slug field in Django is used to store 
    # and generate valid URLs for your dynamically created web pages.
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    slug = models.SlugField("Slug")
    name = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.event.name

    def get_award_links(self):
        return Link.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)

class EventRunReport(Base):
    # module event run report
    # this module is used to store the event awards
    # this is used in the event about us page
    # where user can see the all the
    # run reports of events
    # A slug field in Django is used to store 
    # and generate valid URLs for your dynamically created web pages.
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    slug = models.SlugField("Slug")
    name = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.event.name

    def get_report_links(self):
        return Link.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)


class EventSuccessStoreis(Base):
    # module event success stories
    # this module is used to store the event awards
    # this is used in the event about us page
    # where user can see the all the
    # success stories of events
    # A slug field in Django is used to store 
    # and generate valid URLs for your dynamically created web pages.
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    slug = models.SlugField("Slug")
    name = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.event.name

    def get_success_links(self):
        return Link.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)


class Campaign(Base):
    name                = models.CharField('Title',max_length=100)
    description         = RichTextField(blank=True, null=True)
    slug                = models.SlugField("Campaign URL/Slug")
    widget_icon         = ImageWithThumbsField('Event Widget', upload_to='static/%Y/%m/%d', sizes=((200, 200), (90, 120), (180, 240)), blank=True, null=True,validators=[validate_image])
    start_date          = models.DateField('Campaign start date',blank=True, null=True)
    end_date            = models.DateField('Campaign end date',blank=True, null=True)
    campaign_logo       = ImageWithThumbsField('Campaign Logo', upload_to='static/%Y/%m/%d', sizes=((180, 120), (140, 90), (90, 140)), blank=True, null=True,validators=[validate_image])
    youtube_embedded    = models.URLField('Youtube Embedded Link', blank=True,null=True,help_text = "For example : https://www.youtube.com/embed/23WbluYCUe8")
    campaign_email      = models.EmailField("Contact Email ID", max_length=100)
    mission             = models.TextField('Mission', blank=False, null=True)
    our_work            = models.TextField('Our Work', blank=False, null=True)
    support_for_cause   = models.TextField('Support for the cause', blank=False, null=True)
    our_mission         = models.TextField('Our Mission', max_length=250, blank=False, null=True)
    target_amt          = models.IntegerField('Targetted amount', blank=True, null=True)
 
    def __str__(self):
        return self.name


class EventExtended(Base):
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    our_work = RichTextField(blank=True, null=True)
    mission = RichTextField(blank=True, null=True)
    support_for_the_cause = RichTextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class EventConfig(Base):
    """
        this model is used to config the event
        to  display fundraiser list, cso list, corporates list
        and gallery in frontend
    """
    event = models.ForeignKey(Event,blank=True,null=True,on_delete=models.CASCADE)
    gallery = models.BooleanField(default=True)
    event_type = models.BooleanField(default=True)
    fundraisers = models.BooleanField(default=True)
    corporates = models.BooleanField(default=True)
    csos = models.BooleanField(default=True)
    last_year_highlights = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)+ " " +str(self.event.name)
