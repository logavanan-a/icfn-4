from django.db import models
from NGO.models import *
from mcms.models import *
from django.utils.translation import ugettext_lazy as _
from .views import *

Size_CHOICES = ((u'VS', 'Very Small 0-0.99 Lakh'), (u'S','Small 0-2.99 Crore'),(u'M','Medium 3-7.99 Crore'),(u'L','Large 8 and above'),)
PAYMENT_STATUS_CHOICES = ( (u'Success', u'Success'),(u'Failure', u'Failure'),(u'Pending', u'Pending'),(u'Cancel', u'Cancel'),)
G80_CHOICES = ((u'NA','Not Applicable'),(u'PM','Permanent'),(u'PD','Pending'),(u'VA','Valid'),)
AC35_CHOICES = ((u'NA','Not Applicable'),(u'VA','Valid'),)
FC_CHOICES = ((u'NA','Not Applicable'),(u'VA','Applicable'),)
REGNTYPE_CHOICES= ((u'Trust',u'Trust'),(u'Society',u'Society'),(u'Pvt Ltd Company',u'Pvt Ltd Company'),(u'Section 25 Company',u'Section 25 Company'),(u'Others',u'Others'),)
REGISTER_CHOICES=((0,'Inactive'),(1,'Pending'),(2,'Existing data'))

class CSR(Base):
    # CSR Module
    # used to store all the data of the csr
    # our_mission --> Mission Statement of the NGO
    # work_acheivement --> Work Achievements of the NGO
    # cause can be any of causes NGO wishes
    # youtube_embedd --> Youtube Embedded link should be added
    # primary_focus --> Primary Foucs of the NGO
    # NGO can create atmost 2 projects as of (jan 2016)
    # contact_person --> Deatils of CSR needs to be communicated
    # contact_person include all user requirements
    # reg_no --> CSR registrastion Number
    # established_on --> CSR established date
    # donors can donate for an CSR
    # individual can fundraise for an CSR
    # we_are_on --> Social Network links of an CSR
    # social networks can be Facebook, Twitter etc..
    # this module is not used anywhere in the domain
    # as of january 12 2016
    # A slug field in Django is used to store and generate 
    # valid URLs for your dynamically created web pages.
    contact_person = models.ForeignKey(UserProfile,blank=True,null=True,on_delete=models.CASCADE)
    name = models.CharField('Name of the CSR*', max_length=150)
    reg_no = models.CharField('Charity Registration No*', max_length=40)
    web_address = models.URLField('Web or Blog Address',blank=True)
    validity_80G = models.CharField('80G Validity',choices=G80_CHOICES, max_length=50)
    validity_80G_date = models.DateField('80G Validity Till',blank=True,null=True)
    validity_35AC = models.CharField('35 AC Validity', choices=AC35_CHOICES, max_length=50)
    validity_35AC_date = models.DateField('35AC Validity Till',blank=True,null=True)
    acronym=models.CharField('ACRONYM', max_length=10, blank=True, null=True)
    fcra = models.CharField('FCRA NO *',choices=FC_CHOICES, max_length=50, blank=True, null=True)
    fcra_text = models.CharField('FCRA NO.',max_length=30,blank=True,null=True)
    fcra_date = models.DateField('FCRA Validity Till', blank=True,null=True)
    established_on = models.DateField('Year Founded*', blank=False)
    regn_type = models.CharField('Regn Type*',max_length=30,choices=REGNTYPE_CHOICES) 
    icon = ImageWithThumbsField('Upload Logo', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True ,sizes=((90,120),(80,90),(115,130),(114,146)),help_text = "Upload Logo of size 90x120.", validators=[validate_image])
    latest_fin = models.FileField('Latest Financials', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf")
    size = models.CharField('Turnover/Size*', max_length=3, choices=Size_CHOICES)

    our_mission = RichTextField('Mission Statement*', blank=False)
    work_acheivement = RichTextField('Work Achievements', blank=True, null=True)
    youtube_embedd = models.URLField('Youtube Embedded Link', blank=True)
    slug = models.SlugField(_("Slug"), blank=True)
    fund_utilisation_statement = models.CharField('Fund Utilisation statement',max_length=200,blank=True, null=True)
    black_board_message = RichTextField('Black board messages',blank=True, null=True)
    project = models.ManyToManyField('Projects.Project')
    reference = models.CharField('Reference ID',max_length=500,blank=True, null=True)
    events = models.ManyToManyField('Events.Event', related_name="CSR_events")
    goal_amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="CSR"
        ordering = ['name']


    def get_csr_images(self):
        return Image.objects.filter(content_type__name__iexact="CSR",object_id=self.id)[:5]
    
    def get_csr_atachment(self):
        return Attachment.objects.filter(content_type__name__iexact="CSR",object_id=self.id)

    def get_csr_links(self):
        return Link.objects.filter(content_type__name__iexact="CSR",object_id=self.id)
      
    def get_csr_codes(self):
        return CodeScript.objects.filter(content_type__name__iexact="CSR",object_id=self.id)

    def get_adopted_projects(self):
        return Project.objects.filter(csr__id = self.id, active = True).order_by('id')


class CsrCommunication(Base):
    # module csr communication
    # used to store the communication details like
    # phone number
    # web address
    # fax number
    # mobile number
    # of csr's
    csr = models.ForeignKey(CSR,blank=True,null=True,on_delete=models.CASCADE)
    web_address = models.URLField('Web or Blog Address',blank=True)
    phone1 = models.CharField('Phone1', max_length=15, blank=True, null=True)
    phone2 = models.CharField('Phone2', max_length=15, blank=True, null=True)
    phone3 = models.CharField('Phone3', max_length=15, blank=True, null=True)
    mobile = models.CharField('mobile', max_length=15, blank=True, null=True)
    fax = models.CharField('Fax', max_length=400, blank=True, null=True)

    class Meta:
        db_table = 'csr_csr_communication'

class CsrUsers(Base):
    # module csr users
    # used to store all the csr users
    # subscribed specifies that the user is allowed
    # to view the csr projects
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    phoneno = models.CharField('Mobile Number', max_length=100, blank=True, null=True)
    cname = models.CharField('Company Name', max_length=500, blank=True, null=True)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

class CsrProjects(Base):
    # module csr projects
    # used to store all the csr projects
    # A slug field in Django is used to store and generate 
    # valid URLs for your dynamically created web pages.
    name = models.CharField('Project Name *', max_length=500, blank=True, null=True)
    title = models.CharField('Title *', max_length=500, blank=True, null=True)
    slug = models.SlugField(_("Pick a URL people can remember: *"), max_length=500)
    cause = models.ForeignKey('NGO.Cause', blank=True, null=True,on_delete=models.CASCADE)
    ngo = models.ForeignKey('NGO.NGO', blank=True, null=True,on_delete=models.CASCADE)
    summary = RichTextField('Summary', blank=True, null=True)
    about_us = RichTextField('About Us', blank=True, null=True)
    duration = models.CharField('Duration', max_length=500, blank=True, null=True)
    total_budget = models.CharField('Total Budget', max_length=500, blank=True, null=True)
    amount_in_number = models.IntegerField('Budget in digits', blank=True, null=True)
    location = models.CharField('Location', max_length=500, blank=True, null=True)
    no_to_be_impacted = models.CharField('Numbers to be impacted', max_length=500, blank=True, null=True)
    contact_person = models.CharField('Contact Peron', max_length=500, blank=True, null=True)
    phone = models.CharField('Phone Number', max_length=500, blank=True, null=True)
    email = models.EmailField('Email', max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

