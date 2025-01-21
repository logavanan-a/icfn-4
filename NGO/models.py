from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
'''#from django.contrib.comments.moderation import CommentModerator, moderator'''
from mcms.models import *
from django.core.validators import MaxLengthValidator
from mcms.thumbs import ImageWithThumbsField
from ckeditor.fields import RichTextField
from Projects.models import *
from csr.views import *
from django.db.models import Max
Size_CHOICES = ((u'VS', 'Very Small 0-0.99 Lakh'), (u'S','Small 0-2.99 Crore'),(u'M','Medium 3-7.99 Crore'),(u'L','Large 8 and above'),)
PAYMENT_STATUS_CHOICES = ( (u'Success', u'Success'),(u'Failure', u'Failure'),(u'Pending', u'Pending'),(u'Cancel', u'Cancel'),)
G80_CHOICES = ((u'NA','Not Applicable'),(u'PM','Permanent'),(u'PD','Pending'),(u'VA','Valid'),)
AC35_CHOICES = ((u'NA','Not Applicable'),(u'VA','Valid'),)
FC_CHOICES = ((u'NA','Not Applicable'),(u'VA','Applicable'),)
REGNTYPE_CHOICES= ((u'Trust',u'Trust'),(u'Society',u'Society'),(u'Pvt Ltd Company',u'Pvt Ltd Company'),(u'Section 25 Company',u'Section 25 Company'),(u'Others',u'Others'),)
REGISTER_CHOICES=((0,'Inactive'),(1,'Pending'),(2,'Success'),(3,'Open'))
TYPES_CHOICES=((0,'Keywords'),(1,'Categories'))
CARD_CHOICES  = ((u'PAN','PAN Card'),(u'AC','Aadhar Card'),)
from ckeditor.fields import RichTextField
from datetime import datetime
from icfn_new.settings import HOST_URL,PHOTO_URL,SENDER_MAIL,RECEIVER_MAIL,ADMIN_SENDER_MAIL , ICFN_INFO_MAIL


class Cause(Base):
    # Cause Module
    # Every Ngo, corporate or an individual should have a cause
    # They should know what they are working for.
    name = models.CharField(max_length=100)
    icon = ImageWithThumbsField('Upload Logo', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True ,sizes=((44,60),(90,120),(80,90),(115,130),(114,146), (145,215),(215,145), (228, 151)),help_text = "Upload Logo of size 90x120.")
    description = RichTextField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True,on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug"), blank=True)


    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.name


class Donation(Base):
    # Donation Module
    # This module is used for storing all donations happening on the site.
    # txnid --> Transaction ID sent by the Bank of the transaction
    # amount --> Amount to be donated
    # payment_status
    # SUCCESS --> transaction is successfull
    # Failure --> transaction is failed to some account issues
    # Pending --> transaction is pending
    # Cancel --> transaction has been cancelled by the donor
    # reciept_no --> Reciept Number of the transaction
    # transaction can be for any of 
    # ngo, fundraiser, wishtree, wish, event
    title = models.CharField(_("Title *"), max_length=3)
    first_name = models.CharField(_("First name *"), max_length=80)
    last_name = models.CharField(_("Last name "), max_length=80, blank=True, null=True)
    email = models.EmailField('Email*', max_length=60)
    address1 = models.CharField(_("Address1"), max_length=80, blank=True, null=True)
    address2 = models.CharField(_("Address2"), max_length=80, blank=True, null=True)
    postal_code = models.CharField(_("Pincode*"), max_length=6, blank=True, null=True)
    city = models.CharField(_("City*"), max_length=80, blank=True, null=True)
    state = models.CharField(_("State*"), max_length=80, blank=True, null=True)
    country = models.CharField(_("Country*"), max_length=80, blank=True, null=True)
    amount = models.DecimalField(_("Amount for donation*"),max_digits=15, decimal_places=4)
    deduction_pecentage = models.DecimalField(max_digits=10, decimal_places=1,default=0,blank=True,null=True)
    payment_type = models.CharField(max_length=30,blank=True, null=True)
    paid_on = models.DateTimeField(auto_now_add=True)
    txnid = models.CharField("Transaction Id", max_length=100,blank=True,null=True)
    product_info = models.CharField(_("Product Info"), max_length=80)
    approved_on = models.DateTimeField("Approved On", blank=True, null=True)
    payment_status = models.CharField(_("Payment Status"),max_length=80,choices=PAYMENT_STATUS_CHOICES, blank=True, null=True)
    mode = models.CharField(_("Mode"),max_length=80, blank=True, null=True)
    reciept_no = models.CharField(_("VPC_Reciept No."), max_length=80,blank=True,null=True)
    recieptno_createdby = models.ForeignKey(User,blank=True,null=True,on_delete=models.DO_NOTHING)
    manualrecieptnodate = models.DateTimeField('Mannual Recipt Creation Date',blank=True, null=True)
    project = models.ForeignKey('Projects.Project',blank=True,null=True,on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    ngo=models.ForeignKey('NGO',blank=True, null=True,on_delete=models.DO_NOTHING)
    fundraiser=models.ForeignKey('Fundraiser',blank=True, null=True, related_name="NGO_fundraiser",on_delete=models.DO_NOTHING)
    csrproject = models.ForeignKey('csr.CsrProjects', blank=True, null=True,on_delete=models.DO_NOTHING)
    wish = models.ForeignKey('wishtree.Wish', blank=True, null=True,on_delete=models.DO_NOTHING)
    wishtree = models.ForeignKey('wishtree.WishTree', blank=True, null=True,on_delete=models.DO_NOTHING)
    error_text=models.CharField(max_length=300,blank=True,null=True)
    dtype=models.CharField(max_length=200,blank=True,null=True)
    transaction=models.CharField(max_length=200,blank=True,null=True)
    card_type = models.CharField('Card Type',max_length=200,choices=CARD_CHOICES,blank=True,null=True)
    pan_card = models.CharField('PAN or Adhar Number',max_length=200,blank=True,null=True)
    mobile = models.CharField(max_length=200,blank=True,null=True)
    thank_msg = models.CharField(max_length=450,blank=True,null=True)
    event = models.ForeignKey('Events.Event', blank=True, null=True,on_delete=models.CASCADE)
    payment_details = models.CharField(max_length=1000, blank=True, null=True)
    mail_sent = models.BooleanField(default = False)
    razor_donation = models.BooleanField(default = False)
    paytm_donation = models.BooleanField(default = False)
    pan_card_image = models.FileField('Pan Card', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    pfe = models.ForeignKey('NGO.ParticipateFundraiserinEvent', blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return '%s %s'%(self.first_name,self.last_name)

    @staticmethod
    def is_in_ngo(value):
        res = False
        if NGO.objects.filter(donation__id=self.id):
            res = True
        return res

    def get_amount(self):
        return int(self.amount)


    def get_donation_receipts(self):
        receipt = DonationReceipts.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id)
        return receipt
    def get_donation_deduction(self):
        from Events.models import EventAmountDeduction
        try:
            if self.event:
                ded_obj = EventAmountDeduction.objects.get(Q(start_date__lte=datetime.today().date())&Q(end_date__gte=datetime.today().date()), event=self.event)
                return int(ded_obj.percent)
            else:
                return 5
        except:
            return 5

class OtherDonation(Base):
    # Model name otherDonation
    # send mail for donar
    name = models.CharField(_("name*"), max_length=80)
    email = models.EmailField('Email*', max_length=60)
    amount = models.DecimalField(_("Amount for donation*"),max_digits=15, decimal_places=4)
    company = models.CharField(_("name*"), max_length=80)
    ngo = models.ForeignKey('NGO',blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class NgoKeywords(Base):
    # NGO Keywords Module
    # keywords used to for ngo, csr, fundraiser interests
    name = models.CharField(max_length=200)
    active = models.IntegerField(default=2)

    class Meta:
        # Meta class for NGO communication
        db_table = 'NGO_ngo_keywords'

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.name

class NGO(Base):
    # NGO Module
    # NGO - non-governmental organization
    # NGO can be part of any event they wish to participate
    # our_mission --> Mission Statement of the NGO
    # work_acheivement --> Work Achievements of the NGO
    # cause can be any of causes NGO wishes
    # youtube_embedd --> Youtube Embedded link should be added
    # primary_focus --> Primary Foucs of the NGO
    # NGO can create atmost 2 projects as of (jan 2016)
    # contact_person --> Deatils of NGO needs to be communicated
    # contact_person include all user requirements
    # reg_no --> NGO registrastion Number
    # established_on --> NGO established date
    # donors can donate for an NGO
    # individual can fundraise for an NGO
    # we_are_on --> Social Network links of an NGO
    # social networks can be Facebook, Twitter etc..
    contact_person = models.ForeignKey(UserProfile, related_name="+",on_delete=models.CASCADE)
    name = models.CharField('Name of the CSO', max_length=150)
    register_status=models.PositiveIntegerField(default=1, choices=REGISTER_CHOICES)
    front_image = ImageWithThumbsField('Front Image', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True ,sizes=((90,106),(90,120),(80,90),(115,130),(114,146),(150, 112),(220,124), (203,189)),help_text = "Upload Logo of size 90x120.",validators=[validate_image])
    reg_no = models.CharField('Charity Registration No', max_length=40)
    validity_80G = models.CharField('80G Validity',choices=G80_CHOICES, max_length=50)
    validity_80G_date = models.DateField('80G Validity Till', blank=True,null=True)
    validity_35AC = models.CharField('35 AC Validity', choices=AC35_CHOICES, max_length=50)
    validity_35AC_date = models.DateField('35AC Validity Till',blank=True,null=True)
    acronym=models.CharField('ACRONYM', max_length=10, blank=True, null=True)
    fcra = models.CharField('FCRA',choices=FC_CHOICES, max_length=50, blank=True, null=True)
    fcra_text = models.CharField('FCRA NO',max_length=30,blank=True,null=True)
    fcra_date = models.DateField('FCRA Validity Till', blank=True,null=True)
    a12 = models.CharField('12A',max_length=30,blank=True,null=True)
    established_on = models.DateField('Year Founded')
    regn_type = models.CharField('Regn Type',max_length=30,choices=REGNTYPE_CHOICES, blank=True,null=True)
    icon = ImageWithThumbsField('Upload Logo', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True ,sizes=((45,60),(57,46),(90,106),(90,120),(80,90),(101,72),(100,115),(115,120),(115,130),(114,146),(150, 112)),help_text = "Upload logo of size less than 1Mb.",validators=[validate_image])
    size = models.CharField('Turnover/Size', max_length=3, choices=Size_CHOICES)
    cause = models.ForeignKey(Cause,verbose_name="Primary Cause", blank=True,null=True, related_name="+",on_delete=models.CASCADE)
    secondary_cause = models.ManyToManyField(Cause,verbose_name="Secondary Cause (Click on cause to select and unselect)", blank=True, related_name="cso_secondarycause")
    our_mission = RichTextField('Mission Statement*', help_text="Should not exceed 210 characters")
    work_acheivement = RichTextField('Our Work', blank=True, null=True, help_text="Should not exceed 1900 characters")
    youtube_embedd = models.URLField('Youtube Embedded Link', blank=True,null=True,help_text = "For example : https://www.youtube.com/embed/23WbluYCUe8")
    slug = models.SlugField(_("Your own india cares url"), blank=True,null=True, help_text="For example : http://www.icfn.in/adhm/YOURTEXT/")
    fund_utilisation_statement = models.CharField('Fund Requirement statement',max_length=400, blank=True, null=True, help_text="Should not exceed 350 characters")
    black_board_message = RichTextField('Black board messages', blank=True, null=True, help_text="Should not exceed 190 characters")
    project = models.ManyToManyField('Projects.Project')
    reference = models.CharField('Reference ID',max_length=500,blank=True, null=True)
    accept_donation = models.BooleanField(default=0)
    goal_amount = models.PositiveIntegerField(blank=True,null=True)
    credibility_norms = models.BooleanField('Do you follow the Credibility Alliance norms for transparency and Disclosure', default=False)
    primary_focus = models.CharField('Focus(Primary)', max_length=500, blank=True, null=True)
    secondary_focus = models.CharField('Secondary', max_length=500, blank=True, null=True)
    ngo_keywords = models.ManyToManyField(NgoKeywords)
    latest_fin = models.FileField('Latest Financials', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    audited_balance_sheet = models.FileField('Upload Audited Balance Sheet', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    profit_loss_statement = models.FileField('Upload Profit & Loss Statement', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    undertakng = models.FileField('Upload Undertaking', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    g80_receipt = models.FileField('80G Approval', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    a12_receipt = models.FileField('12A Approval', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    fcra_receipt = models.FileField('FCRA Receipt', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    pan_card = models.FileField('Pan Card', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Pdf/Image")
    we_are_on = models.ManyToManyField(SocialNetwork)
    for_donate_mail = models.BooleanField(default = False)
    for_fundraise_page = models.BooleanField(default = False)
    for_every_month_report = models.BooleanField(default = False)
    display_in_main = models.BooleanField(default = False)
    already_activated = models.BooleanField(default = True)
    frontend_registered = models.BooleanField(default = False)
    meta_title = models.CharField("Meta Page Title", max_length=200, blank = True, null=True)
    meta_description = models.TextField("Meta Description", blank = True, null=True)
    donation_min_amount = models.IntegerField(blank=True, null=True)
    ngos_status = models.IntegerField(default=2)
    
    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.contact_person.user.username + " " + self.name

    class Meta:
        verbose_name_plural="NGO"
        ordering = ['name']

    def get_ngo_images(self):
        return Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id, active=True)

    def get_ngo_atachment(self):
        return Attachment.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id)

    def get_ngo_links(self):
        return Link.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id)

    def get_ngo_codes(self):
        return CodeScript.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id)

    def get_project_count(self):
        return Project.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id, active=True).count()

    def get_ngo_communication(self):
        s = None
        try:
            s = NgoCommunication.objects.get(ngo=self)
        except:
            pass
        return s

    def get_ngo_need(self):
        return Need.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id)

    def get_ngo_volreq(self):
        return VolunteerRequirements.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id)

    def get_donations(self):
        return Donation.objects.filter(ngo=self, payment_status="Success")

    def total_amount(self):
        amt=0
        d = Donation.objects.filter(ngo=self, payment_status="Success")
        for i in d:
            amt = amt + i.amount
        return amt

    def get_offline_donations(self):
        return OfflineDonation.objects.filter(ngo=self)

    def total_offline_amount(self):
        amt = 0
        d = OfflineDonation.objects.filter(ngo=self)
        for i in d:
            amt = amt + i.amount
        return amt

    def get_donation_count(self):
        d = Donation.objects.filter(ngo=self, payment_status='Success').count()
        d1 = OfflineDonation.objects.filter(ngo=self).count()
        tot_dnt = d + d1
        return tot_dnt

    def get_total_donation_amount(self):
        return self.total_offline_amount() + self.total_amount()

    def get_fundraisers(self):
        return Fundraiser.objects.filter(ngo=self, active=True, created_by__is_active=True)

    def get_projects(self):
        return Project.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id, active=True)

    def get_ngo_comm(self):
        return self.get_ngo_communication()

    def get_address(self):
        s = None
        try:
            s = Address.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id).latest('id')
        except:
            pass
        return s

    def get_checkcsos(self):
        from mcms.models import CheckCSO
        return CheckCSO.objects.filter(cso=self, is_created=False)


class NgoCommunication(Base):
    # NGO Communication Module
    # collects the details of an NGO
    ngo = models.ForeignKey(NGO,blank=True,null=True,on_delete=models.CASCADE)
    web_address = models.URLField('Web or Blog Address',blank=True)
    phone1 = models.CharField('Phone1', max_length=15, blank=True, null=True)
    phone2 = models.CharField('Phone2', max_length=15, blank=True, null=True)
    phone3 = models.CharField('Phone3', max_length=15, blank=True, null=True)
    mobile = models.CharField('mobile', max_length=15, blank=True, null=True)
    fax = models.CharField('Fax', max_length=400, blank=True, null=True)

    class Meta:
        # Meta class for NGO communication
        db_table = 'NGO_ngo_communication'

class Need(Base):
    # Need Module
    # collect the need of the NGO
    # donor who wish to donate for the Need can donate.
    name = models.CharField(_("Title*"),max_length=100)
    icon = ImageWithThumbsField(_("Image"),upload_to='static/v2/%Y/%m/%d', blank=True,sizes=((90,120),(180,240),(360,480)), null=True )
    description = RichTextField(blank=True, null=True,max_length=150)
    location = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')


    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.name

    def get_ngo(self):
        try:
            return NGO.objects.get(id=self.object_id)
        except:
            pass

class VolunteerRequirements(Base):
    # Volunteer Requirements Module
    # collect the requirements of the NGO
    # donor who wish to volunteer for the volunteer.
    name = models.CharField(_("Title*"),max_length=100)
    icon = ImageWithThumbsField(_("Image"),upload_to='static/v2/%Y/%m/%d', blank=True,sizes=((90,120),(180,240),(360,480)), null=True )
    description = RichTextField(blank=True, null=True,max_length=150)
    location = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    minimum_period = models.CharField(max_length=100, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')

    class Meta:
        db_table = 'NGO_volunteer_requirements'

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.name

    def get_ngo(self):
        try:
            return NGO.objects.get(id=self.object_id)
        except:
            pass


APPEAL_CHOICES=(('iCare','iCare'),('care champion silver','care champion silver'),('care champion gold','care champion gold'),('Corporate care team 30','Corporate care team 30'),('Corporate care team 20','Corporate care team 20'),)


FUND_TYPE_CHOICES = (('Individual', 'Individual'), ('Corporate', 'Corporate'))
class FundraiserType(Base):
    # Fundraiser Type Module
    # tells whether fundraiser is an Individual or Corporate
    # color --> used to display in all pages of the fundraisers
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(_("Pick a URL people can remember: *"))
    color = models.CharField(max_length=100, blank=True, null=True)
    event_index = models.IntegerField(blank=True, null=True)
    fund_choice = models.CharField(blank=True, null=True, choices=FUND_TYPE_CHOICES, max_length=100)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return '%s'%(self.name)

    def get_fundraiser(self):
        return Fundraiser.objects.filter(fundraiser_type__id = self.id)

    def get_fundraisertype_details(self):
        try:
            return FundraiserTypeDetails.objects.get(ftype__id = self.id)
        except:
            return 0

class FundraiserTypeDetails(Base):
    # Fundraiser type details module
    # used to provide an option for the user to download the fundraiser forms
    # minimum_pledge --> Minimum amount for the Pledge
    # pledge amount varies from one fundraiser type to another
    ftype = models.ForeignKey(FundraiserType,blank=True,null=True,on_delete=models.CASCADE)
    download_form = models.FileField('Download Form', upload_to='static/v2/%Y/%m/%d', blank=True, null=True)
    minimum_pledge = models.CharField("Minimum Pledge", max_length=200, blank=True, null=True, help_text = "Display in Front End")
    enter_in_digits = models.CharField('Enter in digits',max_length=200, blank=True, null=True)
    reg_support = models.BooleanField(default=False)
    car_parking = models.BooleanField(default=False)

    class Meta:
        db_table = 'NGO_fundraisertype_details'

class Fundraiser(Base):
    # Fundraiser Module
    # created to raise funds for the NGO's
    # goal_amount --> amount that fundraiser wish to achieve
    # Fundraiser should have any one of NGO or project they will work for.
    # thank_msg --> Message from the fundraiser that will be sent to donor
    # if they donate for the fundraising page
    company_name = models.CharField("Company Name ", max_length=200, blank=True,  null=True)
    fundraiser_type = models.ForeignKey(FundraiserType, blank=True, null=True, related_name="+",on_delete=models.CASCADE)
    title = models.CharField("Fundraising Page Title(100 Character Max):*", max_length=100)
    slug = models.SlugField(_("Pick a URL people can remember: *"))
    icon = ImageWithThumbsField('Icon',upload_to='v2/%Y/%m/%d',sizes=((62,62),(90,120),(126,122),(127,169),(139,132),(140,130),(180,240),(360,480),(160,166), (203,189), (101, 134)), blank=True, null=True ,validators=[validate_image])
    description = RichTextField('Your Appeal to People :*',help_text="Should not exceed 2000 characters")
    thank_msg = RichTextField('Write a thank you message:(This message goes to your donors as soon as they donate) :*', help_text="Should not exceed 2000 characters" ,blank=True, null=True)
    goal_amount = models.IntegerField('Amount of money you hope to raise:*', blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name="+",on_delete=models.CASCADE)
    donation = models.ManyToManyField('Donation',related_name="Fundraiser_Donation")
    project = models.ForeignKey('Projects.Project',blank=True,null=True, related_name="+",on_delete=models.CASCADE)
    ngo = models.ForeignKey('NGO',blank=True,null=True, related_name="+",on_delete=models.CASCADE)
    atype=models.CharField("Appeal Type ",max_length=200,choices=APPEAL_CHOICES ,blank=True,  null=True)
    display_name = models.CharField("Display Name", max_length=200, blank=True, null=True)
    meta_title = models.CharField("Meta Page Title", max_length=200, blank = True, null=True)
    meta_description = models.TextField("Meta Description", blank = True, null=True)
    fund_status = models.IntegerField(default=2)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return '%s %s '%(self.created_by.first_name, self.created_by.last_name)

    def get_fundraiser_images(self):
        return Image.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id, active=True)

    def get_donations(self):
        return Donation.objects.filter(fundraiser=self, payment_status='Success')

    def get_offline_donations(self):
        return OfflineDonation.objects.filter(fundraiser=self)

    def get_offline_total_amount(self):
        amt=0
        d = OfflineDonation.objects.filter(fundraiser=self).filter(event__active=True)
        for i in d:
            amt = amt + i.amount
        return amt

    def get_donation_count(self):
        d = Donation.objects.filter(fundraiser=self, payment_status='Success').filter(event__active=True).count()
        d1 = OfflineDonation.objects.filter(fundraiser=self).filter(event__active=True).count()
        tot_dnt = d + d1
        return tot_dnt

    def get_total_donation_amount(self):
        return self.get_offline_total_amount() + self.total_amount()

    def get_total_amount_online(self):
        amt=0
        d = Donation.objects.filter(fundraiser=self, payment_status='Success').filter(event__active=True)
        for i in d:
            amt = amt + i.amount
        return amt

    def total_amount(self):
        amt=0
        offamt = 0
        d = Donation.objects.filter(fundraiser=self, payment_status='Success').filter(event__active=True)
        d1 = OfflineDonation.objects.filter(fundraiser=self).filter(event__active=True)
        for i in d:
            amt = amt + i.amount
        for offd in d1:
            offamt = offamt + offd.amount
        tot_amt = amt + offamt
        return tot_amt

    def percentage_donated(self):
        try:
            donated = float(self.total_amount()) * 100 / float(self.goal_amount)
        except:
            donated = 0
        return int(donated)

    def large_donated(self):
        max_donated = Donation.objects.filter(fundraiser=self, payment_status='Success').filter(event__active=True).aggregate(Max('amount'))['amount__max']
        return Donation.objects.filter(amount = int(max_donated),fundraiser=self, payment_status='Success').filter(event__active=True)[:1]

    def latest_donated(self):
        return Donation.objects.filter(fundraiser = self, payment_status='Success').filter(event__active=True).latest('id')

    def latest_offline_donated(self):
        return OfflineDonation.objects.filter(fundraiser=self).filter(event__active=True).latest('id')

    def get_user_profile(self):
        try:
            return UserProfile.objects.get(user = self.created_by)
        except:
            return None
    

    def get_fundraiser_icon(self):
        try:
            if self.icon.file:
                image = str(PHOTO_URL +'static'+self.icon.url)     
        except:
            try:
                if self.ngo.icon.file:
                    image = str(PHOTO_URL +'static'+self.ngo.icon.url)
            except:
                image = PHOTO_URL +"/static/frontend/img/no-image.jpg"
                # image = PHOTO_URL +"/static/v2/2021/11/12/no-image.jpg"
        return image


class NgoAppeals(Base):
    #Module NgoAppeals
    # used to store ngo appeals
    # ngo can appeal for some need
    # donors can donate to the appeal
    ngo = models.ForeignKey(NGO,blank=True,null=True,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    appeal_for = models.CharField(max_length=100)

    class Meta:
        db_table = 'NGO_ngo_appeals'

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return '%s - %s'%(self.ngo.name, self.appeal_for)

PLAN_CHOICES = (('Basic','Basic'), ('Essential', 'Essential'), ('Premium', 'Premium'))
PAYMENT_STATUS_CHOICES = ( (u'Success', u'Success'),(u'Failure', u'Failure'),(u'Pending', u'Pending'),(u'Cancel', u'Cancel'),)
class NgoSubscription(Base):
    # Module NgoSubscription
    # used to store subscribtions of ngo
    # this models is not used anywhere in the website
    # ngo specifies ngo that is subscribed
    # Plan choices
    # Basic
    # Essential
    # Premium
    ngo = models.ForeignKey(NGO,blank=True,null=True,on_delete=models.CASCADE)
    plan = models.CharField(choices=PLAN_CHOICES, max_length=100)
    valid_from = models.DateField()
    valid_to = models.DateField()
    duration = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField()
    payment_type = models.CharField(max_length=30, blank=True, null=True)
    paid_on = models.DateTimeField(auto_now_add=True)
    txnid = models.CharField("Transaction Id", max_length=100)
    product_info = models.CharField(_("Product Info"), max_length=80)
    approved_on = models.DateTimeField("Approved On", blank=True, null=True)
    payment_status = models.CharField(_("Payment Status"),max_length=80,choices=PAYMENT_STATUS_CHOICES)
    mode = models.CharField(_("Mode"),max_length=80, blank=True, null=True)
    reciept_no = models.CharField(_("VPC_Reciept No."), max_length=80)
    error_text=models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        db_table = 'NGO_ngo_subscription'

PAYMENT_MODE_CHOICES = (('Cash','Cash'), ('Cheque/DD', 'Cheque/DD'), ('Bank transfer', 'Bank transfer'), ('NGO Website', 'CSO Website'))
class OfflineDonation(Base):
    # Module Offline Donation
    # used to store all the offline donations
    # fundraiser can create an offline doantion they made through
    # Bank Transfer
    # Cash
    # Cheque/DD
    # donor has to be basic information about the donations they made
    donor_name = models.CharField(_("Name of the Donor *"), max_length=200)
    email = models.EmailField('Email of the Donor *', max_length=100)
    landline_no = models.CharField("Landline Number",max_length=200,blank=True,null=True)
    mobile = models.CharField("Mobile Number", max_length=200,blank=True,null=True)
    amount = models.DecimalField(_("Amount for donation *"),max_digits=15, decimal_places=2)
    card_type = models.CharField('Card Type',max_length=200,choices=CARD_CHOICES,blank=True,null=True)
    pan_card = models.CharField("Pan Card / Adhar Card", max_length=200,blank=True,null=True)
    address1 = models.TextField(_("Residential Address of the Donor"), blank=True, null=True)
    address2 = models.TextField(_("Office address of the Donor"), blank=True, null=True)
    payment_mode = models.CharField("Payment Mode", max_length=200, choices=PAYMENT_MODE_CHOICES, blank=True, null=True)
    cheque_no = models.CharField("Cheque Number", max_length=200, blank=True, null=True)
    bank_name = models.CharField("Bank Name", max_length=200,blank=True,null=True)
    image_of_cheque = models.FileField('Image of Cheque',upload_to='static/v2/%Y/%m/%d', blank=True, null=True )
    event = models.ForeignKey('Events.Event', blank=True, null=True,on_delete=models.CASCADE)
    fundraiser=models.ForeignKey('Fundraiser',blank=True, null=True, related_name="Donate_NGO_fundraiser",on_delete=models.CASCADE)
    ngo=models.ForeignKey('NGO',blank=True, null=True,on_delete=models.CASCADE)
    date = models.CharField("Date of Donation", max_length=30, blank=True, null=True)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.donor_name
        
    def get_donation_receipts(self):
        receipt = DonationReceipts.objects.filter(content_type=ContentType.objects.get_for_model(self),object_id=self.id)
        return receipt    

    class Meta:
        db_table = 'NGO_offline_donation'

# CORPORATE_CHOICES = [('Team-10','Team-10'), ('Team-12','Team-12'), ('Team-15', 'Team-15'), ('Team-25', 'Team-25'), ('Team-30', 'Team-30'), ('Team-40', 'Team-40'), ('Team-45', 'Team-45'), ('Team-60', 'Team-60'), ('Team-100', 'Team-100')]
# f = FundraiserType.objects.filter(active=True)
# for ft in f:
#     CORPORATE_CHOICES.append((ft.name,ft.name))
class DuplicateCorporates(Base):
    # Module Duplicate corporates
    # Used to store all the duplicate corporates
    # this corporates are used in marathon events will be displayed
    # on marathon events home page
    # corporates has to be from
    # Team-10
    # Team-25
    # Team-40
    # no_of_teams specifies no of teams participated
    event = models.ForeignKey('Events.Event', blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField('Corporate Name', max_length=200)
    ngo = models.ForeignKey(NGO, blank=True, null=True,on_delete=models.CASCADE)
    team = models.CharField("Select Team", max_length=200, blank=True, null=True)
    fundraiser_type  = models.ForeignKey(FundraiserType,blank=True,null=True,on_delete=models.CASCADE)
    no_of_teams = models.IntegerField(default=1)

    many_ngos = models.ManyToManyField(NGO, related_name="duplicate_corporate_csos")

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.name

    class Meta:
        db_table = 'NGO_duplicate_corporates'

class Volunteers(Base):
    # Module Volunteers
    # used to store volunteers data
    # used for volunteers who are ready to volunteer forCORPORATE_CHOICES ngo
    # Volunteers have to provide there basic details like
    # name
    # location
    # phone_no
    # email
    # skill
    # message
    ngo = models.ForeignKey(NGO, blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=100)
    location = models.CharField('Location', max_length=100, blank=True, null=True)
    phone_no = models.CharField('Tel No', max_length=100, blank=True, null=True)
    email = models.EmailField('Email', max_length=100, blank=True, null=True)
    skill = models.CharField('Skill', max_length=100, blank=True, null=True)
    message = models.TextField('Message', max_length=200, blank=True, null=True)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.name

GENDER_CHOICES = ( (u'M', u'Male'), (u'F', u'Female'),)
class CharityBib(Base):
    donation = models.ForeignKey(Donation,blank=True,null=True,on_delete=models.CASCADE)
    dob = models.DateField('Date of Birth', blank=True,null=True)
    gender = models.CharField("Gender", max_length=80, blank=True, null=True, choices=GENDER_CHOICES)
    phone_no = models.CharField("Phone Number", max_length=10, blank=True, null=True)
    emergency_name = models.CharField("Emergency Name", max_length=80, blank=True, null=True)
    emergency_number = models.CharField("Emergency Number", max_length=80, blank=True, null=True)
    friend_number1 = models.CharField("Friend Number1", max_length=20, blank=True, null=True)
    friend_number2 = models.CharField("Friend Number2", max_length=20, blank=True, null=True)
    target_hrs = models.CharField("Target Hours", max_length=20, blank=True, null=True)
    target_min = models.CharField("Target Minutes", max_length=20, blank=True, null=True)
    proof = models.FileField('Upload ID Proof', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True, help_text = "Upload files in Pdf/Image")

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return "%s - %s"%(self.donation.first_name, self.donation.last_name)

DONATION_MAILER_CHOICES = (('Donation', 'Donation'), ('Registration', 'Registration'), ('AdminMails', 'AdminMails'))
class DoantionMailer(Base):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')
    html = models.CharField(max_length=100, blank=True, null=True)
    mailtype = models.CharField(max_length=100, blank=True, null=True, choices=DONATION_MAILER_CHOICES)
    text = models.TextField(blank=True, null=True)
    sender = models.CharField(max_length=100, blank=True, null=True)
    receiver = models.CharField(max_length=200, blank=True, null=True)
    functionname = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        try:
            return "%s-%s-%s"%(self.text, self.content_type, self.object_id)
        except:
            return self.text

class ParticipateFundraiserinEvent(Base):
    ngo = models.ForeignKey('NGO',blank=True,null=True,on_delete=models.CASCADE)
    event = models.ForeignKey('Events.Event',blank=True,null=True,on_delete=models.CASCADE)
    fundraiser_type = models.ForeignKey(FundraiserType, blank=True, null=True, related_name="fundraiser_typeparticipated",on_delete=models.CASCADE)
    fundraisers = models.ManyToManyField('Fundraiser', related_name="participate_fundraiser_in_event")
    user = models.ForeignKey(User, blank=True, null=True, related_name="fundraiser_user",on_delete=models.CASCADE)
    is_donated = models.BooleanField(default=False)
    is_page_created = models.BooleanField(default=False)
    is_old_user = models.BooleanField(default=False)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return "%s - %s"%(self.ngo.name, self.event.name)


############################# Full history Module ################################
class DashboardWidgetsTypes(Base):
    name = models.CharField(max_length=50)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.name

class DashboardChartWidgets(Base):
    title = models.CharField(max_length=100)
    slug = models.SlugField("Slug", max_length=300,null=True, blank=True)
    label = models.CharField(max_length=100)
    widgettype = models.ForeignKey(DashboardWidgetsTypes,on_delete=models.CASCADE)
    widgetquery_sql = models.TextField()
    chart_header = models.CharField(max_length=250, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)


    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return str(self.title) + '-' + str(self.label)


AWARD_TYPE_CHOIES = (('CSOs','CSOs'),('Fundraiser','Fundraiser'),('Corporate','Corporate'))
class TopEventAwards(Base):
    ################### Top-event awards #######
    # independant event awards feature 
    # title, description, image, award_type and order
    # for the top three csos, fundraisers, and corporate
    ###################
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = ImageWithThumbsField('image',upload_to='static/v2/%Y/%m/%d',sizes=((62,62),(90,120),(126,122),(127,169),(139,132),(140,130),(180,240),(360,480),(160,166), (203,189), (101, 134)), blank=True, null=True )
    award_type = models.CharField(max_length=100, blank=True, null=True, choices=AWARD_TYPE_CHOIES)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.title



class DonationReceipts(Base):
    pdf_file = models.FileField(upload_to='static/attachment/%Y/%m/%d', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    
    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return str(self.id)


class HomePageSpeak(Base):
    headline = models.CharField("Main title", max_length=350, blank=True, null=True)
    speech_title = models.CharField("Story title",max_length=350, blank=True, null=True)
    speech_video = models.URLField('Youtube Embedded Link')
    speach = RichTextField('Story',blank=True, null=True)
    byline = models.CharField(max_length=350, blank=True, null=True)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.headline

class AccrossTheCountry(Base):
    ################ Home Page Accross the country #######
    # title, description, banner, video
    # in home page accorss the country section is created
    # ########################################### 
    title = models.CharField(max_length=350, blank=True, null=True)
    description = RichTextField('Description',blank=True, null=True)
    banner  = ImageWithThumbsField('Upload background image',upload_to='static/v2/%Y/%m/%d',sizes=((62,62),(90,120),(126,122),(127,169),(139,132),(140,130),(180,240),(360,480),(160,166), (203,189), (101, 134)), blank=True, null=True ,validators=[validate_image])
    video = models.URLField('Youtube Embedded Link')

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.title or u'None'



class ReachOutHeading(Base):
    ##################### Reach out headings ##########
    # in reach out page headline, banner, description, and icon
    # displaying in first part of reachout page
    # icon is reachout page icon
    ##############################################
    headline = models.CharField(max_length=350, blank=True, null=True)
    banner = ImageWithThumbsField('banner',upload_to='static/v2/%Y/%m/%d',sizes=((62,62),(90,120),(126,122),(127,169),(139,132),(140,130),(180,240),(360,480),(160,166), (203,189), (101, 134)), blank=True, null=True ,validators=[validate_image])
    description = RichTextField('description',blank=True, null=True)
    icon = ImageWithThumbsField(_("Icon"),upload_to='static/v2/%Y/%m/%d', blank=True,sizes=((90,120),(180,240),(360,480)), null=True ,validators=[validate_image])

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.headline


class ReachOutProgram(Base):
    #################### Reach out programs ###############
    # name, description, organization name, image description, header
    # listed in reach out program and its not depends on any even or anything
    #########################################################
    name = models.CharField(max_length=350, blank=True, null=True)
    organization_name = models.CharField(max_length=350, blank=True, null=True)
    image = ImageWithThumbsField('image',upload_to='static/v2/%Y/%m/%d',sizes=((62,62),(90,120),(126,122),(127,169),(139,132),(140,130),(180,240),(360,480),(160,166), (203,189), (101, 134)), blank=True, null=True ,validators=[validate_image])
    description = models.TextField(blank=True, null=True)
    header = models.CharField(max_length=350, blank=True, null=True)
    header_description = RichTextField('header_description',blank=True, null=True)

    def __str__(self):
        # unicode method
        # it will not create additional data in database
        return self.name


MEDIA_CHOICES = (('GIF','GIF'),('VIDEO','VIDEO'),('PHOTO','PHOTO'))
class HomePageMediaContent(Base):
    mediatype = models.CharField('Banner Type',max_length=100, blank=True, null=True, choices=MEDIA_CHOICES)
    name = models.CharField('Banner Text',max_length=100, blank=True, null=True)
    media_banner = models.FileField('Upload Banner', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True,help_text = "Upload files in Video/Gif/Image")
    url = models.URLField('Youtube Embedded Link', blank=True,null=True,help_text = "For example : https://www.youtube.com/embed/23WbluYCUe8")

    def __str__(self):
        return self.name


class Classification(Base):
    name = models.CharField(max_length=200,blank=True, null=True)
    order = models.PositiveIntegerField()
    parent = models.ForeignKey('self', blank=True, null=True,on_delete=models.CASCADE)
    types  = models.PositiveIntegerField(choices=TYPES_CHOICES)

    def __str__(self):
        return self.name


class Cso_Classification_Relation(Base):
    ngo = models.ForeignKey('NGO',blank=True, null=True,on_delete=models.CASCADE)
    classification = models.ManyToManyField('Classification',blank=True)
    keywords = models.ManyToManyField('CsoClassificationKeyword',blank=True)
    def __str__(self):
        return str(self.id)


class CsoClassificationKeyword(Base):
    name = models.CharField(max_length=200,blank=True, null=True)
    def __str__(self):
        return self.name



class ForeignerDonationDetails(Base):
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    ngo = models.ForeignKey(NGO,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        

class ShareDetails(Base):
    key = models.CharField(max_length=2000,blank=True,null=True)
    title = models.CharField('Name of the CSO', max_length=150)
    description = RichTextField('Mission Statement*', help_text="Should not exceed 210 characters")
    image = models.CharField(max_length=3000,blank=True,null=True)

    def __str__(self):
        return self.key
