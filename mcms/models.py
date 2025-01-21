from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.contrib import admin
from mcms.thumbs import ImageWithThumbsField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User,UserManager
from mcms.manager import *
import six
from csr.views import *
#--name prefix choices--------------#
# choices are mr,miss,mrs,dr,sr,colonel
# ------end----------------------#

NAME_PREFIX_CHOICES = (('Mr.','Mr'), ('Ms.','Ms'),('Mis','Miss'),('Mrs','Mrs'),('Dr','Dr'),('Sr','Sr'),('Col','Colonel'))
#----gender choices-------------#
GENDER_CHOICES = ( (u'M', u'Male'), (u'F', u'Female'),)
#---usertype choices ---------------#
#--it can be ngo, individual or fundraiser----------#
USERTYPE_CHOICES = ( (u'1', u'NGO'), (u'2', u'Individual'),(u'3', u'Fundraiser'),)

# class BaseContentBase(models.base.ModelBase):

#     def __iter__(self):
#         return self.objects.all().__iter__()

#     @staticmethod
#     def register(mdl):
#         if (not hasattr(mdl, 'Meta')) or getattr(
#                 getattr(mdl, '_meta', None),
#                 'abstract', True
#         ):
#             return mdl

#         class MdlAdmin(admin.ModelAdmin):
#             list_display = [
#                 '__str__'] + getattr(mdl, 'admin_method', []) + [i.name for i in mdl._meta.fields]
#             filter_horizontal = [i.name for i in mdl._meta.many_to_many]

#         if hasattr(mdl, 'Admin'):
#             class NewMdlAdmin(mdl.Admin, MdlAdmin):
#                 pass
#             admin.site.register(mdl, NewMdlAdmin)

#         else:
#             admin.site.register(mdl, MdlAdmin)

#     def __new__(cls, name, bases, attrs):
#         mdl = super(BaseContentBase, cls).__new__(cls, name, bases, attrs)
#         BaseContentBase.register(mdl)
#         return mdl


# class Base(six.with_metaclass(BaseContentBase, models.Model)):
class Base(models.Model):
    # ---------comments-----------------------------------------------------#
    # BaseContent is the abstract base model for all
    # the models in the project
    # This contains created and modified to track the
    # history of a row in any table
    # This also contains switch method to deactivate one row if it is active
    # and vice versa
    # ------------------------ends here---------------------------------------------#
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = BaseQuerySet.as_manager()

    class Meta:
        #-------------------meta----------------------#
        # Don't create a table in database
        # This table is abstract
        #--------------------ends here--------------------#
        abstract = True


class Country(Base):
    #-------country model---------------------#
    # Similar to country in real world
    #                                        Country
    # ------ends here-------------------------#
    name = models.CharField('Country Name', max_length=400)

    def __str__(self):
    # ---unicode method---#ID
    # Don't create a table in database
    # return country name
    # ---------ends here--------------#
        return self.name


class State(Base):
    #------ model state-------------#
    # country is a foriegnkey
    #------ends here----------# 
    country = models.ForeignKey(Country,blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField('State Name', max_length=400)

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name


class Section(Base):
    #------ model section-------------#
    # to create sections
    # with name icon,description
    #------ends here----------# 
    name = models.CharField('Name', max_length=200)
    icon = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d', sizes=((90,120),(180,240),(360,480)),blank=True,  null=True ,validators=[validate_image])
    description = RichTextField(blank = True, null = True)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen", max_length=60)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name

    def get_section_images(self):
    # -------get section images
    # model method 
    # to get images related to section
    # ------ends--------------#
        return Image.objects.filter(content_type = ContentType.objects.get_for_model(self), object_id=self.id)

    def get_section_atachment(self):
    # -------get section atachment
    # model method 
    # to get attachments related to section
    # ------ends--------------#
        return Attachment.objects.filter(content_type = ContentType.objects.get_for_model(self), object_id=self.id)

    def get_section_links(self):
    # -------get section links
    # model method 
    # to get link related to section
    # ------ends--------------#
        return Link.objects.filter(content_type = ContentType.objects.get_for_model(self), object_id=self.id)
      
    def get_section_codes(self):
    # -------get section codes
    # model method 
    # to get codescript related to section
    # ------ends--------------#
        return CodeScript.objects.filter(content_type = ContentType.objects.get_for_model(self), object_id=self.id)


class Article(Base):
    #------ model article-------------#
    # to create articles
    # with section,summary,description,image
    #------ends here----------# 
    name = models.CharField('Name', max_length=200)
    section = models.ForeignKey(Section,blank=True,null=True,on_delete=models.CASCADE)
    summary = models.CharField("Byline/ Summary", blank=True, null=True, max_length=1000)
    description = RichTextField()
    image = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d', sizes=((90,120),(180,240),(287,124),(360,480)),blank=True,  null=True ,validators=[validate_image])
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen", max_length=60)

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name

    def get_article_images(self):
    # -------get article_images
    # model method 
    # to get image related to article
    # ------ends--------------#
        return Image.objects.filter(content_type__name__iexact="article",object_id=self.id)

    def get_article_atachment(self):
    # -------get article_atachment
    # model method 
    # to get attachment related to article
    # ------ends--------------#
        return Attachment.objects.filter(content_type__name="article",object_id=self.id)

    def get_article_links(self):
    # -------get article_links
    # model method 
    # to get link related to article
    # ------ends--------------#
        return Link.objects.filter(content_type__name="article",object_id=self.id)

    def get_article_codes(self):
    # -------get article_codes
    # model method 
    # to get codescript related to article
    # ------ends--------------#
        return CodeScript.objects.filter(content_type__name="article",object_id=self.id)

NEWS_CHOICES = ( (u'India Cares News', u'India Cares News'), (u'Sector Specific News', u'Sector Specific News'),)
class News(Base):
    #------ model news-------------#
    # to create news with section,summary, description, valid from,valid to
    #------ends here----------# 
    event = models.ForeignKey('Events.Event',blank=True,null=True,on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=200)
    news_type = models.CharField(max_length=100, choices=NEWS_CHOICES)
    section = models.ForeignKey(Section,blank=True,null=True,on_delete=models.CASCADE)
    summary = models.CharField("Byline/ Summary", blank=True, null=True, max_length=400)
    description = RichTextField(blank = True, null = True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    link = models.CharField('Url', max_length=500,blank=True, null=True)
    image = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d', sizes=((90,120),(180,240),(287,124),(360,480)),blank=True,  null=True ,validators=[validate_image])


    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name
# ----site choices----------------#
# site can be general,adhm,tcsworld10k,ffc,uts,cricket for cause,vodafonecycling
# --------ends -----------------#
SITE_CHOICES = ( (u'general', u'general'), (u'ADHM', u'ADHM'), (u'TCSWorkld10k', u'TCSWorkld10k'), (u'FFC', u'FFC'), (u'UTS', u'UTS'), (u'Cricket for cause', u'Cricket for cause'), (u'VodafoneCycling', u'VodafoneCycling'),)
class Gallery(Base):
    # ------gallery------------#
    # to create gallery
    # with site choices,event,name,description,front image
    # --------ends----------------#
    choice = models.CharField(max_length=100, choices=SITE_CHOICES)
    event = models.ForeignKey('Events.Event', blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = RichTextField(blank=True, null=True)
    front_image = ImageWithThumbsField(upload_to='static/v2/%Y/%m/%d', sizes=((90,120),(180,240),(360,480), (281, 186)),blank=True,  null=True,validators=[validate_image])
    link = models.CharField('Url for album', max_length=500,blank=True, null=True )

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name

    def get_images(self):
    # -------get images
    # model method 
    # to get image related to gallery
    # ------ends--------------#
        return Image.objects.filter(content_type=ContentType.objects.get(model__iexact = 'gallery'),object_id=self.id, active=True)

class CodeScript(Base):
    #------ model-------------#
    #------ends here----------# 
    name = models.CharField(max_length=60)
    description = models.TextField("Code to be inserted", 
                        blank=True, null=True, max_length=800)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')


    def __str__ (self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name



class Attachment(Base):
    #------ model Attachment-------------#
    # this is to attach any file related documents
    # this is also content type
    # so we can use table for any model
    #------ends here----------# 
    name = models.CharField(max_length=60)
    attach_file = models.FileField(upload_to='static/v2/%Y/%m/%d', blank=True, null=True)
    description = models.CharField("Description", blank=True, null=True, max_length=300)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name



class Image(Base):
    #------ model Image-------------#
    # this is create media
    # we are using content type so we can use this media part anywhere
    #------ends here----------# 
    image = ImageWithThumbsField(upload_to='static/v2/%Y/%m/%d', sizes=((90,120), (100,100),(120,120),(180,240),(360,480),(930,300)),blank=True,null=True,help_text="Image size should be 930x300 pixels",validators=[validate_image])
    name = models.CharField("Caption * ", blank=True, null=True, max_length=50)
    description = models.CharField("Description", blank=True, null=True, max_length=300)
    URL = models.URLField("Link url", max_length=200, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')


    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return '%s'%(self.name)



class Link(Base):
    # --------link-----------------------#
    # Class describes cms links
    # using genric foriegnkey
    # ---ends here----------------------#
    name = models.CharField(max_length=100)
    image = ImageWithThumbsField(upload_to='static/v2/%Y/%m/%d', sizes=((90,
                                 120), (180, 240), (360, 480)), blank=True,
                                 null=True)
    URL = models.CharField('Link url', max_length=200, blank=True)
    description = models.CharField('Description', blank=True, null=True,
                                   max_length=300)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name

    @staticmethod
    def latest_link(*args, **kwargs):
    # -----static method ------------#
    # latest link
    # return s
    # --------ends here-------------#
        try:
            s =  Link.objects.filter(*args, **kwargs).latest('id')
        except:
            s = None
        return s

class Address(Base):
    #------ Address model-------------#
    # this is to create address for ngo,csr etc.
    # we are using content type 
    # so that we can use this model anywhere
    # just by calling model method  
    #------ends here----------# 
    address1 = models.CharField('Address1', max_length = 100, blank=True, null=True)
    address2 = models.CharField('Address2', max_length = 100, blank=True, null=True)
    country = models.ForeignKey('Country', blank = True, null = True,on_delete=models.CASCADE)
    state = models.ForeignKey('State', blank = True, null = True,on_delete=models.CASCADE)
    city = models.CharField('City', max_length = 100, blank=True, null=True)
    mobile = models.CharField('Mobile', max_length = 100, blank=True, null=True)
    pincode = models.CharField('Pincode', max_length = 100, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')


    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return "%s - %s - %s" %(self.state, self.city, self.address1)


class StaffType(Base):
    #------staff type model-------------#
    # to define staff type for an example:trustees
    #------ends here----------# 
    name=models.CharField(max_length=60)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen",max_length=60)

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name

    @classmethod
    def get_trustees(self):
        # model method
        # to get staff of type trustees
        #---ends here-----#
        return Staff.objects.filter(staffType__slug = 'trustees', active = True)

    @classmethod
    def get_staffs(self):
    # -----------get staffs--------------#
    # model method StaffType
    # to get staff of type staff
    #--ends here-----------#
        return Staff.objects.filter(staffType__slug = 'staff', active = True)

    class Meta:
    # ----------meta-----------------#
    # ----this is to change filed names in databse table 
    # table name is staff type
    # field name is mcms_staff_type
    # -----ends here---------#
        db_table = 'mcms_staff_type'

class Staff(Base):
    #------ staff model-------------#
    # to create team members of icfn
    # with prefix, name,gender,stafftype, summary and profile text,image,webURL
    #------ends here----------# 
    prefix = models.CharField("Prefix *", max_length=10, choices=NAME_PREFIX_CHOICES)
    name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField("Gender *", max_length=1, choices=GENDER_CHOICES)
    staffType = models.ForeignKey('StaffType', blank=True, null=True,on_delete=models.CASCADE)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen *", max_length=60)
    summary = models.CharField("summary", blank=True, null=True, max_length=200)
    profile_text = RichTextField(blank=True, null = True)
    image = models.ImageField(upload_to='static/v2/%Y/%m/%d', blank=True, null=True )
    webURL = models.URLField("Web URL", blank=True, null=True, max_length=60)
    display_order = models.PositiveIntegerField('Displaying order', blank=True, null=True)

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return u'%s %s '%(self.prefix, self.name)

class EventType(Base):
    #------ model event type -------------#
    # this is to create eventtype
    #------ends here----------# 
    name = models.CharField(max_length=100)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen",max_length=60)

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name

    class Meta:
    # ----------meta-----------------#
    # ----this is to change filed names in databse table 
    # table name is event type
    # field name is mcms_event_type
    # -----ends here---------#
        db_table = 'mcms_event_type'

class OurEvents(Base):
    #------ our events model-------------#
    # this is to create events with event type,name,start year,end year,amount 
    # raised, description,image
    #------ends here----------# 
    event_type = models.ForeignKey(EventType,blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField('Event Name', max_length=200)
    start_year = models.DateField(blank=True,null=True)
    end_year = models.DateField(blank=True,null=True)
    amount_raised = models.PositiveIntegerField()
    description = RichTextField(blank=True, null=True)
    image = ImageWithThumbsField(upload_to = 'static/v2/images/%Y/%m/%d', sizes=((90,120),(180,240),(360,480)),blank=True,  null=True )

    def __str__(self):
        #----unicode method -------#
        # don't create a table in database
        # ends here
        return self.name

    class Meta:
        # ----this is to change database table names
        # our events is the table name
        # mcms_our_events is the field name we are going to change
        verbose_name_plural = 'Our Events'
        db_table = 'mcms_our_events'

class Salutations(Base):
    #------Salutations model-------------#
    # we are giving salutation like mr,ms to the names
    #------ends here----------# 
    name = models.CharField('Name*', max_length=100)

    def __str__(self):
        
        return self.name

class UserProfile(Base):
    #------ userprofile model-------------#
    # to create userprofile with titile, user,usertype
    #------ends here----------# 
    title = models.ForeignKey(Salutations, blank=True, null=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='static/v2/%Y/%m/%d', blank=True, null=True )
    user = models.ForeignKey(User,blank=True, null=True,on_delete=models.CASCADE)
    usertype = models.CharField("UserType ", max_length=100, choices=USERTYPE_CHOICES, blank=True, null=True)
    user_status = models.IntegerField(default=2)

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # if it is not username
        # return first name
        # else return username
        # ---ends here-----------#
        if not self.user.username:
            return self.user.first_name
        else:
            return self.user.username

class UserDetails(Base):
    #------ model-------------#
    # this is to store user details with user, username and password
    #------ends here----------# 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # return username
        # ---ends here-----------#
        return self.username


class IndividualActivation(models.Model):
    #------ model-------------#
    # user activation
    # with active field is a boolean field
    #------ends here----------# 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        #----unicode method -------#
        # don't create a table in database
        # return username
        # ---ends here-----------#
            return self.user.username

class Invite(Base):
    #------ invite model-------------#
    # send invitations to admin 
    # including name,ngo website link, contact_person, email,phone,your_name,
    # email,comments
    #------ends here----------# 
    name = models.CharField("CSO Name",max_length=100)
    url = models.URLField("CSO Website Link", max_length=200,blank=True,null=True)
    contact_person = models.CharField("CSO Contact Person ",max_length=100,blank=True,null=True)
    email = models.EmailField("CSO Email Id *")
    phone = models.CharField("CSO Contact Number ", max_length=15,blank=True,null=True)
    your_name = models.CharField("Your Name *",max_length=100)
    your_email = models.EmailField("Your Email Id *")
    comments = models.TextField("Your message to the CSO",blank=True,null=True)

    def __str__(self):
        #----unicode method -------#
        # don't create a table in database
        # return name
        # ---ends here-----------#
        return self.name


class HomeBanner(Base):
    #------ homebanner model-------------#
    # this is to provide space to add banner for websites
    #------ends here----------# 
    name = models.CharField("Image name",max_length=100)
    image = ImageWithThumbsField(upload_to = 'static/v2/images/%Y/%m/%d', 
                                    sizes=((90, 120), (180, 240), (360, 480), 
                                    (1200, 556), (655, 403)), blank=True, null=True,validators=[validate_image])

    def __str__(self):
        #----unicode method -------#
        # don't create a table in database
        # return name
        # ---ends here-----------#
        return self.name

class Requests(Base):
    #------ requests model-------------#
    # -----to send requests
    # with name,email,phone,message
    #------ends here----------# 
    name = models.CharField('Name', max_length=400,blank=True,null=True)
    email = models.EmailField("Email*", max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    message = models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
    #----unicode method -------#
        # don't create a table in database
        # return name
        # ---ends here-----------#
        return self.name

class Contactus(Base):
    #------ contactus model-------------#
    # to contact the client 
    # to write any query from user to superadmin
    # which includes phone and mobile number
    #------ends here----------# 
    summary = models.CharField('Summary', max_length=400,blank=True,null=True)
    description = RichTextField(blank=True, null = True)
    phone1 = models.CharField('Phone1', max_length=15,blank=True,null=True)
    phone2 = models.CharField('Phone2', max_length=15,blank=True,null=True)
    phone3 = models.CharField('Phone3', max_length=15,blank=True,null=True)
    mobile1 = models.CharField('Mobile1', max_length=15,blank=True,null=True)
    mobile2 = models.CharField('Mobile2', max_length=15,blank=True,null=True)

    def __str__(self):
        #----unicode method -------#
        # don't create a table in database
        # return summary
        # ---ends here-----------#
        return self.summary

    def get_address(self):
        # ----model method-----------#
        # return address objects of model name called contactus
        # ------ends here-----------#
        return Address.objects.filter(content_type = ContentType.objects.get_for_model(self), object_id=self.id)


class Tags(Base):
    #------ Tags model-------------#
    # inheriting base class
    # saving tag object using slug
    #------ends here----------# 
    name = models.CharField('Tag Name', max_length=400)
    slug = models.SlugField("Slug")

    def __str__(self):
        #----unicode method -------#
        # don't create a table in database
        # ---ends here-----------#
        return self.name


class Blog(Base):
    #------ blog model-------------#
    # inheriting base class to set active or deactive
    # this model is to create blogs
    # in general scenario blogs contains title,summary,description,blog date,
    # if anyimage want to add we can create image, author, tag name, can attach media
    # and able to provide link
    #------ends here----------# 
    title = models.CharField('Blog title', max_length=400, blank=True, null=True)
    slug = models.SlugField("Slug")
    summary = models.TextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    blog_date = models.DateField(blank=True, null=True)
    image = ImageWithThumbsField(upload_to='static/v2/images/%Y/%m/%d', 
            sizes=((90, 120), (180, 240), (360, 480), (217, 143), (773, 267), (233, 131)), blank=True, null=True)
    author = models.CharField(max_length=400, blank=True, null=True)
    tags = models.ManyToManyField(Tags)
    attachment = models.FileField(upload_to='static/v2/%Y/%m/%d', blank=True, null=True)
    youtube_embedd = models.CharField('Youtube Embedded Link', max_length=200, blank=True,null=True)

    def __str__(self):
        #----unicode method -------#
        # don't create a table in database
        # ---ends here-----------#
        return self.title

    def get_absolute_url(self):
        # ---model method to get url
        return "/blog/%s/" % (self.slug)

class Quotes(Base):
    # -------- Quotes Model ------- #
    # used in home page
    # designation
    # -------- ends here ---------- #
    name = models.CharField(max_length=500, blank=True, null=True)
    designation = models.CharField("Designation", max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    summary = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    qdate = models.DateField(blank=True, null=True)
    image = ImageWithThumbsField(upload_to='static/v2/%Y/%m/%d', 
            sizes=((90, 120), (180, 240), (170, 170)), blank=True, null=True)

    def __str__(self):
        return self.name

class OurInitiatives(Base):
    # -------- OurInitiatives Model ------- #
    # used in home page
    # initiatives from the india cares
    # -------- ends here ---------- #
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    url = models.CharField("Link", max_length=200,blank=True,null=True)
    dates = models.DateField(blank=True, null=True)
    image = ImageWithThumbsField(upload_to='static/v2/%Y/%m/%d', 
            sizes=((90, 120), (112, 112)), blank=True, null=True,validators=[validate_image])

    def __str__(self):
        return self.name

from bs4 import BeautifulSoup
import requests
import urllib3,sys
import html5lib

class AroundTheWeb(Base):
    # -------- AroundTheWeb Model ------- #
    # used to store information of other website links
    # -------- ends here ---------- #
    title = models.CharField(max_length=300, blank=True, null=True)
    description = RichTextField(blank=True, null = True)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen", max_length=100,blank=True, null=True)
    source = models.CharField(max_length=500, blank=True, null=True)
    summary = models.TextField(blank=True, null = True)
    link = models.CharField(max_length=1000, blank=True, null = True)
    image = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d',
                                 sizes=((90,120), (180, 240), (270, 172), (270, 185), (210, 140)), blank=True, null=True)
    image_url = models.TextField(blank=True, null = True)

    def __str__(self):
        return self.title

#    def save(self, *args, **kwargs):
#        if self.link and not (self.title or self.description):
#            # optionally, use 'html' instead of 'lxml' if you don't have lxml installed
#            hdr = {'User-Agent': 'Mozilla/5.0'}
#            req = urllib2.Request(self.link, headers=hdr)
#            page = urllib2.urlopen(req)
#            soup = BeautifulSoup(page, 'html5lib')
#            self.title = soup.title.string.encode('utf-8')
#            meta_tags = soup.find_all('meta')
#            meta = soup.find('meta',property="og:image")
#            try:
#                description = soup.find('meta',property="og:description").encode('utf-8')
#            except:
#                description = soup.find('meta',name="description").encode('utf-8')
#            self.image_url = meta['content']
#            for tag in meta_tags:
#                if 'name' in tag.attrs and tag.attrs['name'].lower() in ['description', ]:
#                    setattr(self, tag.attrs['name'].lower(), tag.attrs['content'])
#        super(AroundTheWeb, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        import lxml.html
        url = self.link
        t = lxml.html.parse(url)
        self.title = t.find(".//title").text
        for i in t.findall(".//meta"):
            if i.values()[0] == "og:image":
                self.image_url = i.values()[1]
        if not self.image_url:
            for j in t.findall(".//img")[0].items():
                if j[0] == 'src':
                    self.image_url = j[1]
        super(AroundTheWeb, self).save(*args, **kwargs)

PAGE_CHOICES = ((u'aboutus', u'aboutus'), (u'contactus', u'contactus'), (u'event', u'event'), (u'login', u'login'), (u'thankyou', u'thankyou'), (u'Food For Change', u'Food For Change'), (u'Under The Stars', u'Under The Stars'), (u'Seva Mela', u'Seva Mela'), (u'others', u'others'))
class PageBanners(Base):
    event = models.ForeignKey('Events.Event',blank=True,null=True,on_delete=models.CASCADE)
    ptype = models.CharField("Page", max_length=100, choices=PAGE_CHOICES, blank=True, null=True)
    banner1 = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d',
                                 sizes=((90,120), (180, 240), (293, 194)), blank=True, null=True)
    banner2 = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d',
                                 sizes=((90,120), (180, 240), (293, 194)), blank=True, null=True)
    banner3 = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d',
                                 sizes=((90,120), (180, 240), (293, 194)), blank=True, null=True)

    def __str__(self):
        return self.ptype


class Iccontent(Base):
    name = models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.name


class Iccontentdetails(Base):
    iccontent = models.ForeignKey(Iccontent,blank=True, null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True,null=True)
    description = RichTextField(blank=True, null = True)
    image = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d', sizes=((90,120),(180,240),(287,124),(360,480)),blank=True,null=True ,validators=[validate_image])
    url = models.URLField(max_length=200,blank=True,null=True)
    numb = models.PositiveIntegerField('Number', blank=True, null=True)

    def __str__(self):
        return self.title


FILETYPE_CHOICES = (('Annual Report','Annual Report'),('Docket','Docket'))
class AnnualReport(Base):
    name = models.CharField(max_length=100,blank=True,null=True)
    event = models.ForeignKey('Events.Event',blank=True,null=True,on_delete=models.CASCADE)
    image = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d', sizes=((90,120),(180,240),(219,215),(360,480)),blank=True,null=True ,validators=[validate_image])
    filetype = models.CharField("FileType ", max_length=100, choices=FILETYPE_CHOICES,default='Annual Report')
    url = models.CharField(max_length=200,blank=True,null=True)
    attach_file = models.FileField(upload_to='static/v2/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.name

class UserUpdateContent(Base):
    user = models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE)
    old_email = models.CharField(max_length=200, blank=True, null=True)
    new_email = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.email


from datetime import date, datetime
YEAR_CHOICES = []
for r in range(2015, 2050):
    YEAR_CHOICES.append((str(r),r))

class HomePageContent(Base):
    year = models.CharField(max_length=20, choices=YEAR_CHOICES)
    our_reach = models.CharField(max_length=20, blank=True, null=True)
    fundraisers = models.CharField(max_length=20, blank=True, null=True)
    donors = models.CharField(max_length=20, blank=True, null=True)
    amount_raised = models.CharField(max_length=20, blank=True, null=True)
    beneficiaries = models.CharField(max_length=20, blank=True, null=True)
    visitors = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.year

#from NGO.models import *
class CheckCSO(Base):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200)
    uid = models.CharField(max_length=200, blank=True, null=True)
    cso = models.ForeignKey('NGO.NGO',blank=True, null=True,on_delete=models.CASCADE)
    is_created = models.BooleanField(default=False)
    mobile = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.cso.name

class CSOUsers(Base):
    cso = models.ForeignKey('NGO.NGO',blank=True, null=True,on_delete=models.CASCADE)
    is_parent = models.BooleanField(default=False)
    user = models.ForeignKey(User,blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.cso.name, self.user.email)

class CSORequestToParticipate(Base):
    cso = models.ForeignKey('NGO.NGO',blank=True, null=True,on_delete=models.CASCADE)
    is_joined = models.BooleanField(default=False)
    user = models.ForeignKey(User,blank=True, null=True,on_delete=models.CASCADE)
    event = models.ForeignKey('Events.Event',on_delete=models.CASCADE)
    last_year_report = models.FileField(upload_to='static/v2/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.cso.name, self.user.email, self.event.name)

class CSOChangeUserDetails(Base):
    cso = models.ForeignKey('NGO.NGO', blank=True, null=True,on_delete=models.CASCADE)
    old_user = models.ForeignKey(User, related_name="old_user",blank=True, null=True,on_delete=models.CASCADE)
    new_user = models.ForeignKey(User, related_name="updated_to_user",blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.old_user, self.new_user)
