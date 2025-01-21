from django.db import models
from mcms.models import *
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from mcms.thumbs import ImageWithThumbsField
from django.utils.translation import ugettext_lazy as _
from NGO.models import *
PR_Pending, PR_Started, PR_In_Progress, PR_Completed = range(4)
from django.db.models import Max

# Choices for project
# this will specfiy the project state
# following are the states
# Pending
# Started
# InProgress
# Completed
PROJECT_STATUS = (
            (PR_Pending, 'Pending'),
            (PR_Started, 'Started'),
            (PR_In_Progress, 'In Progress'),
            (PR_Completed, 'Completed'),
)


class ProjectCause(Base):
    # module project cause
    # it stores the cause of the projects
    # Every project should have cause
    # slug way of generating a valid URL, generally using data already obtained.
    # module name has been updated from Project_Cause
    # to
    # ProjectCause
    # due to sonarqube issue
    title = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(_("Slug"), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Projects_project_cause'

class SocialNetwork(Base):
    # module social network
    # it stores all the social networks 
    # every ngo, project can add there social networks links
    # module name has been updated from Social_Network
    # to
    # SocialNetwork
    # due to sonarqube issue
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Projects_social_network'

class Project(Base):
    # module project
    # it stores all the projects 
    # slug way of generating a valid URL, generally using data already obtained.
    # problem specifies the problem of the project
    # how_project_will_solve_problem specifies
    # how to solve the problem for solution
    # long_term_impact specifies
    # how that solution impact long term
    # we_are_on are the social networks
    # of the projects
    # following are unique data of the project
    # upload_pdf
    # for_donate_mail
    # for_fundraise_page
    # for_every_month_report
    # people_supported specifies
    # the number of people supporting the project
    title = models.CharField(_("Title of the Project:"),max_length=100)
    icon = ImageWithThumbsField(upload_to='static/v2/images/%Y/%m/%d', sizes=((90,120),(120,120),(180,240),(360,480), (132, 220)),blank=True,  null=True )
    slug = models.SlugField(_("Slug"), blank=True)
    problem = RichTextField('The problem:',blank=True, null=True, help_text = "maximum 200 characters")
    how_project_will_solve_problem = RichTextField('How will this project solve the problem?:',blank=True, null=True, help_text = "maximum 200 characters")
    long_term_impact = RichTextField('What is the long term impact of this project?:',blank=True, null=True, help_text = "maximum 200 characters")
    start_date = models.DateField('Start date', blank = True, null = True)
    end_date = models.DateField(blank=True, null=True)
    target_amount = models.PositiveIntegerField('Goal', blank=True, null=True)
    cause = models.ForeignKey('NGO.Cause', null=True, blank=True,on_delete=models.CASCADE)
    we_are_on = models.ManyToManyField(SocialNetwork)
    project_status = models.IntegerField("Project Status", choices = PROJECT_STATUS)
    upload_pdf = models.FileField(upload_to='static/v2/%Y/%m/%d', blank=True, null=True)
    for_donate_mail = models.BooleanField(default = False)
    for_fundraise_page = models.BooleanField(default = False)
    for_every_month_report = models.BooleanField(default = False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')

    people_supported = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_project_images(self):
        return Image.objects.filter(content_type__name__iexact="project",object_id=self.id, active=True)

    def get_donations(self):
        from NGO.models import Donation
        return Donation.objects.filter(payment_status='Success', project=self)

    def large_donated(self):
        from NGO.models import Donation
        max_donated = Donation.objects.filter(project=self, payment_status='Success').aggregate(Max('amount'))['amount__max']
        return Donation.objects.filter(amount = int(max_donated), project=self, payment_status='Success')[0]

    def latest_donated(self):
        from NGO.models import Donation
        return Donation.objects.filter(project=self, payment_status='Success').latest('id')

    def get_total_amount_online(self):
        from NGO.models import Donation
        amt=0
        d = Donation.objects.filter(project=self, payment_status='Success')
        for i in d:
            amt = amt + i.amount
        return amt

    def percentage_donated(self):
        try:
            donated = float(self.get_total_amount_online()) * 100 / float(self.target_amount)
        except:
            donated = 0
        return int(donated)

    def get_ngo(self):
        from NGO.models import NGO
        return NGO.objects.get(pk=self.object_id)

    def get_fundraisers(self):
        from NGO.models import Fundraiser
        return Fundraiser.objects.filter(project=self, active=True, created_by__is_active=True)

    def get_project_links(self):
        return Link.objects.filter(content_type__name__iexact="project",object_id=self.id, active=True)

# following are the registered models of project application
# ProjectCause
# Project
#register_model(ProjectCause)
#register_model(Project)
