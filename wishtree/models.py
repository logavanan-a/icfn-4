from django.db import models
from django.db.models import Sum
from mcms.models import *
from NGO.models import Cause, Donation, NGO
from mcms.thumbs import ImageWithThumbsField
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

Need_Choices = (('Cash', 'Cash'), ('Non-Cash', 'Non-Cash'))
G80_CHOICES = ((u'NA', 'Not Applicable'),(u'PM', 'Permanent'),(u'PD', 'Pending'),(u'VA', 'Valid'),)
AC35_CHOICES = ((u'NA','Not Applicable'),(u'VA','Valid'),)
Usertype_CHOICES = ((u'Ngo','CSO'),(u'Corporate','Corporate'), (u'Group','Group'))
A12_CHOICES = ((u'NA','Not Applicable'),(u'PM','Permanent'),(u'PD','Pending'),(u'VA','Valid'),)
UNIT_CHOICES = ((u'days', 'days'), (u'kgs', 'kgs'), (u'hours', 'hours'), (u'months', 'months'), (u'units', 'units'))
TREE_CHOICES = (('Event', 'Event'), ('Others', 'Others'))

# Create your models here.
class WishType(Base):
    need_type = models.CharField("Need Type", max_length=200, choices=Need_Choices)
    name = models.CharField("Wish Type", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'wishtree_wish_type'

class WishtreeCity(Base):
    state = models.ForeignKey('mcms.State',on_delete=models.CASCADE)
    name = models.CharField("City name *", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'wishtree_wishtree_city'

ARCHIVE_CHOICES = ((0,"No"),(1,"Yes"))
class WishTree(Base):
    name = models.CharField("Make Your own Link *", max_length = 500, blank=True, null=True, help_text = ".icfn.in")
    wtype = models.CharField("Tree Type", max_length=200, choices=TREE_CHOICES)
    event = models.ForeignKey('Events.Event',blank=True,null=True,on_delete=models.CASCADE)
    code = models.CharField("Make Your URL*", max_length=50)
    slug = models.SlugField(max_length = 500)
    image = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d', 
                                 sizes=((90, 120), (180, 240), (360, 480)),
                                 blank=True, null=True )
    description = RichTextField("Description", blank=True, null=True)
    cause = models.ManyToManyField(Cause, blank=True)
    no_of_wish = models.CharField("Number of Wishes*", max_length=20, blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE)
    is_main_page = models.BooleanField(default=False)
    home_page_wishes = models.CharField("Home page wish count", max_length=50, blank=True, null=True)
    archive = models.PositiveIntegerField(choices=ARCHIVE_CHOICES,default=0,blank=True, null=True)


    class Meta:
        db_table = 'wishtree_wish_tree'

    def get_ngo(self):
        ngo = None
        try:
            # ngo = WishtreeNgo.objects.get(user=self.created_by)
            ngo = WishtreeNgo.objects.get(user=self.created_by,active=True)
        except:
            pass
        return ngo

    def __str__(self):
        return "%s - %s" %(self.name, self.code)

    def get_wishes(self):
        return Wish.objects.filter(wishtree=self, active=True)

    def get_online_donations_amount(self):
        total_d = Donation.objects.filter(wishtree=self, payment_status='Success').aggregate(Sum("amount"))['amount__sum']
        if not total_d:
            total_d = 0
        return int(total_d)

    def get_donations(self):
        return Donation.objects.filter(wishtree=self, payment_status='Success')

    def get_other_donations(self):
        return OtherDonations.objects.filter(wishtree=self)

    def total_other_donations(self):
        total_donations = self.get_other_donations().aggregate(Sum("quantity_of_gift"))['quantity_of_gift__sum']
        if not total_donations:
            total_donations = 0
        return int(total_donations)

    def get_target_other_donations(self):
        target_amt = self.get_wishes().filter(wishtype__need_type='Non-Cash').aggregate(Sum("target"))['target__sum']
        if not target_amt:
            target_amt = 0
        return int(target_amt)

    def get_target_donation_amount(self):
        target_amt = self.get_wishes().filter(wishtype__need_type='Cash').aggregate(Sum("target"))['target__sum']
        if not target_amt:
            target_amt = 0
        return int(target_amt)

    def percentage_donated(self):
#        wishes = []
#        for i in Wish.objects.filter(finished=False):
#            if int(i.get_completed_amount()) >= int(i.target):
#                wishes.append(i)
#        for i in wishes:
#            i.finished = True
#            i.save()
        if self.is_main_page:
            no_of_wishes = Wish.objects.filter(parent=None).count()
            finished_wishes = Wish.objects.filter(finished=True, parent=None).count()
            try:
                donated = float(finished_wishes) * 100 / float(no_of_wishes)
            except:
                donated = 0
            return int(donated)
        else:
            no_of_wishes = self.get_wishes().count()
            finished_wishes = self.get_wishes().filter(finished=True).count()
            try:
                donated = float(finished_wishes) * 100 / float(no_of_wishes)
            except:
                donated = 0
            return int(donated)

    def get_completed_wishes(self):
        if self.is_main_page:
            finished_wishes = Wish.objects.filter(finished=True).count()
        else:
            finished_wishes = self.get_wishes().filter(finished=True).count()
        return finished_wishes

class WishtreeCampaigns(Base):
    name = models.CharField(max_length=100, blank=True, null=True)
    wishtree = models.ForeignKey('Wishtree',blank=True,null=True,on_delete=models.CASCADE)
    start_date = models.DateField("Start Date", blank=True, null=True)
    end_date = models.DateField("End Date", blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Wish(Base):
    parent = models.ForeignKey('self', blank=True, null=True,on_delete=models.CASCADE)
    wishtree = models.ForeignKey(WishTree,blank=True,null=True,on_delete=models.CASCADE)
    wishtype = models.ForeignKey(WishType, blank=True, null=True, verbose_name=_('Wish Type *'),on_delete=models.CASCADE)
    name = models.CharField("Wish Title *", max_length=500, blank=True, null=True)
    benefit_name = models.CharField("Beneficiary Name", max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=500)
    requirement = RichTextField("Requirement *")
    quantity = models.IntegerField('Quantity *', default=0)
    cost_per_unit = models.CharField("Cost per Unit *", max_length=100, blank=True, null=True)
    target = models.CharField("Target Amount/No of Hrs *", max_length=200)
    start_datetime = models.DateTimeField("Start DateTime *", blank=True, null=True)
    end_datetime = models.DateTimeField("End DateTime *", blank=True, null=True)
    place_to_deliver = RichTextField("Address to deliver *", blank=True, null=True)
    city = models.CharField("City", max_length=200, blank=True, null=True)
    unit = models.CharField("Type", max_length=200, choices=UNIT_CHOICES, blank=True, null=True)
    cause = models.ManyToManyField(Cause, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')
    image = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d', 
                                 sizes=((90, 120), (180, 240), (360, 480)),
                                 blank=True, null=True )
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_online_donations_amount(self):
        total = 0
        child_amt = 0
        total_d = Donation.objects.filter(wish=self, payment_status='Success').aggregate(Sum("amount"))['amount__sum']
        child = Wish.objects.filter(parent=self)
        child_amount = [Donation.objects.filter(wish=i, payment_status='Success').aggregate(Sum("amount"))['amount__sum'] for i in child if i.is_donated()]
        child_amount = [0 if v is None else v for v in child_amount]
        if child_amount is not None:
            child_amt = sum(child_amount)
        if not total_d:
            total_d = 0
        if child_amt:
            total = int(total_d) + int(child_amt)
        else:
            total = int(total_d)
        return total

    def get_offline_donations_amount(self):
        total = 0
        child = ''
        child_amt = 0
        total_d = OtherDonations.objects.filter(wish=self, is_completed=True).aggregate(Sum("quantity_of_gift"))['quantity_of_gift__sum']
        child = Wish.objects.filter(parent=self)
        child_amount = [OtherDonations.objects.filter(wish=i, is_completed=True).aggregate(Sum("quantity_of_gift"))['quantity_of_gift__sum'] for i in child if i.is_donated()]
        child_amount = [0 if v is None else v for v in child_amount]
        if child_amount:
            child_amt = sum(child_amount)
        if not total_d:
            total_d = 0
        if child_amt:
            total = int(total_d) + int(child_amt)
        else:
            total = int(total_d)
        return total

    def get_total_ipledge_quantity(self):
        total = 0
        child_amt = 0
        total_d = IpledgeDonation.objects.filter(wish=self, is_fullfilled=True).aggregate(Sum("quantity"))['quantity__sum']
        child = Wish.objects.filter(parent=self)
        child_amount = [IpledgeDonation.objects.filter(wish=i, is_fullfilled=True).aggregate(Sum("quantity"))['quantity__sum'] for i in child]
        child_amount = [0 if v is None else v for v in child_amount]
        if child_amount:
            child_amt = sum(child_amount)
        if not total_d:
            total_d = 0
        if child_amt:
            total = int(total_d) + int(child_amt)
        else:
            total = int(total_d)
        return total

    def get_total_ipledge_amount(self):
        total = 0
        child_amt = 0
        total_d = IpledgeDonation.objects.filter(wish=self, is_fullfilled=True).aggregate(Sum("amount"))['amount__sum']
        child = Wish.objects.filter(parent=self)
        child_amount = [IpledgeDonation.objects.filter(wish=i, is_fullfilled=True).aggregate(Sum("amount"))['amount__sum'] for i in child]
        child_amount = [0 if v is None else v for v in child_amount]
        if child_amount:
            child_amt = sum(child_amount)
        if not total_d:
            total_d = 0
        if child_amt:
            total = int(total_d) + int(child_amt)
        else:
            total = int(total_d)
        return total

    def get_completed_quantity(self):
        completed = 0
        child_amount = []
        if self.wishtype.need_type == 'Cash':
            if self.get_online_donations_amount() >= 0:
                completed = int(self.get_online_donations_amount() / int(self.cost_per_unit))
            completed = int(completed) + int(self.get_total_ipledge_quantity())
        if self.wishtype.need_type == 'Non-Cash':
            completed = OtherDonations.objects.filter(wish=self, is_completed=True).count()
            child = Wish.objects.filter(parent=self)
            if child:
                child_amount = [OtherDonations.objects.filter(wish=i, is_completed=True) for i in child if i.is_donated()]
            if child_amount:
                completed = completed + len(child_amount)
        return completed

    def get_pending_quantity(self):
        return self.quantity - self.get_completed_quantity()

    def get_pending_quantity_new(self):
        # return 12
        val_return =  self.quantity - self.get_completed_quantity()
        if val_return  < 12:
            return val_return
        else:
            return 12



    def is_donated(self):
        val = False
        if self.wishtype.need_type == 'Cash':
            check1 = Donation.objects.filter(wish=self, payment_status='Success')
            check2 = IpledgeDonation.objects.filter(wish=self, is_fullfilled=True)
            if check1 or check2:
                val = True
        elif self.wishtype.need_type == 'Non-Cash':
            check3 = OtherDonations.objects.filter(wish=self, is_completed=True)
            if check3:
                val = True
        return val

    def get_completed_amount(self):
        amount = 0
        if self.cost_per_unit:
            amount = int(self.get_online_donations_amount() + int(self.get_total_ipledge_amount()))
        return amount

    def get_remaining_amount(self):
        amount = int(self.target) - int(self.get_completed_amount())
        return amount

    def is_completed(self):
        val = False
        if (self.wishtype.need_type == 'Cash' and self.get_completed_quantity() >= int(self.quantity)) or (self.wishtype.need_type == 'Non-Cash' and self.get_offline_donations_amount() >= int(self.target)):
            val = True
        return val

class NonCashDonations(Base):
    wish = models.ForeignKey(Wish,on_delete=models.CASCADE)
    required = models.CharField("Actual Requirement*", max_length=200)
    completed = models.CharField("Completed Requirement*", max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.wish.name

    class Meta:
        db_table = 'wishtree_non_cash_donations'

class OtherDonations(Base):
    wish = models.ForeignKey(Wish,on_delete=models.CASCADE)
    wishtree = models.ForeignKey(WishTree,on_delete=models.CASCADE)
    name = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    address1 = models.CharField(max_length=500, blank=True, null=True)
    address2 = models.CharField(max_length=500, blank=True, null=True)
    quantity_of_gift = models.CharField(max_length=50, blank=True, null=True)
    time_required = models.CharField(max_length=50, blank=True, null=True)
    no_of_hours = models.CharField(max_length=50, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.wish.name

    class Meta:
        db_table = 'wishtree_other_donations'

class WishtreeNgo(Base):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    contact_person = models.CharField('Contact Person*',max_length=500)
    reg_no = models.CharField('Ngo Registration No*', max_length=40, blank=True,null=True)
    validity_80G = models.CharField('80G Validity',choices=G80_CHOICES, max_length=50, blank=True,null=True)
    validity_80G_date = models.DateField('80G Validity Till', blank=True,null=True)
    validity_35AC = models.CharField('35 AC Validity', choices=AC35_CHOICES, max_length=50, blank=True,null=True)
    validity_35AC_date = models.DateField('35AC Validity Till',blank=True,null=True)
    summary = RichTextField("Summary", blank=True, null=True)
    logo = ImageWithThumbsField('Upload Logo', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True ,sizes=((45,60),(57,46),(90,106),(90,120),(80,90),(101,72),(100,115),(115,120),(115,130),(114,146),(150, 112)),help_text = "Upload Logo of size 90x120.")
    website = models.URLField('Website',blank=True,null=True)
    pan_card = models.CharField("Pan Card Number", max_length=200,blank=True,null=True)
    utype = models.CharField('User Type', choices=Usertype_CHOICES, max_length=50, blank=True,null=True)
    focus_statement = models.TextField('Focus Statement', max_length=500, blank=True,null=True)
    a12 = models.CharField('12A', choices=A12_CHOICES, max_length=500)
    a12_pdf = models.FileField('Upload A12 Receipt *', upload_to='static/v2/%Y/%m/%d', blank=True, null=True, help_text = "Upload files in Pdf")
    G80_pdf = models.FileField('Upload 80G Reciept *', upload_to='static/v2/%Y/%m/%d', blank=True, null=True, help_text = "Upload files in Pdf")
    pan_card_pdf = models.FileField('Upload Pan Card Reciept *', upload_to='static/v2/%Y/%m/%d', blank=True, null=True, help_text = "Upload files in Pdf")
    city = models.ForeignKey(WishtreeCity, blank=True, null=True,on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishtree_wishtree_ngo'

    def __str__(self):
        return self.name

    def get_address(self):
        try:
            return Address.objects.get(content_type=ContentType.objects.get_for_model(self),object_id=self.id)
        except:
            return None


class IpledgeDonation(Base):
    wish = models.ForeignKey(Wish,on_delete=models.CASCADE)
    wishtree = models.ForeignKey(WishTree,on_delete=models.CASCADE)
    first_name = models.CharField('First Name *', max_length=500, blank=True, null=True)
    last_name = models.CharField('Last Name *', max_length=500, blank=True, null=True)
    email = models.EmailField('Email *', blank=True, null=True)
    mobile = models.CharField('Mobile *', max_length=50, blank=True, null=True)
    address1 = models.CharField('Address *', max_length=500, blank=True, null=True)
    address2 = models.CharField(max_length=500, blank=True, null=True)
    delivery_in_date = models.CharField("I will Deliver on",max_length=50, blank=True, null=True)
    is_fullfilled = models.BooleanField(default=False)
    amount = models.CharField("Amount *", max_length=200, blank=True, null=True)
    quantity = models.IntegerField("Quantity *", default=0)

    def __str__(self):
        return '%s - %s' %(self.first_name, self.wish.name)

    class Meta:
        db_table = 'wishtree_ipledge_donation'

class WishtreeImage(Base):
    home_image = models.FileField('Home Background', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True)
    inner_logo = models.FileField('Logo', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True)
    tree_image = models.FileField('Login Image', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True)
    cso_image = models.FileField('CSO page Background', upload_to='static/v2/%Y/%m/%d', blank=True,  null=True)
    start_datetime = models.DateTimeField("Start DateTime", blank=True, null=True)
    end_datetime = models.DateTimeField("End DateTime", blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' %(self.start_datetime, self.end_datetime)
