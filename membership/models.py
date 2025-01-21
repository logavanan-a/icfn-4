from django.db import models
from mcms.models import *
# Create your models here.

class Members(Base):
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null = True)
    short_summary = RichTextField(blank=True, null = True)
    image = ImageWithThumbsField(upload_to = 'static/v2/%Y/%m/%d', sizes=((140,64),(272,287), (247,148)),blank=True,null=True )
    url = models.URLField(max_length=200,blank=True,null=True)
    contact_person = models.CharField(max_length=100,blank=True,null=True)
    mobile = models.CharField('Mobile', max_length = 15, blank=True, null=True)
    country = models.ForeignKey(Country, blank = True, null = True,on_delete=models.CASCADE)
    state = models.ForeignKey(State, blank = True, null = True,on_delete=models.CASCADE)
    city = models.CharField('City', max_length = 100, blank=True, null=True)
    pincode = models.CharField('Pincode', max_length = 15, blank=True, null=True)
    documnt = models.FileField(upload_to='static/v2/%Y/%m/%d', blank=True, null=True)
    
    def __str__(self):
        return self.name

