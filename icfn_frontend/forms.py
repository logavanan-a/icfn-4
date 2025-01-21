


from django import forms
from NGO.models import *
from mcms.models import UserProfile
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from mcms.thumbs import ImageWithThumbsField
from django.contrib.auth.models import User
from Projects.models import Project
from Events.models import *
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets
from captcha.fields import ReCaptchaField

class FundraiserFormBk(forms.ModelForm):
    # --------------- FundraiserFormBk form-----------#
    # this is a model form
    # model name : fundraiser
    # filtering ngo objects and storing in a ngolist variable
    # excluding: donation,active,atype,project, companyname
    #----------ends------------------------------#
    EVT_CHOICES =( ('','---------'), (u'Marathon', u'Marathon'), (u'Campaign', u'Campaign'))
    created_by = UserModelChoiceField(queryset=User.objects.filter(is_active=True).order_by('first_name'))
    event_type = forms.ChoiceField(label="Event Type",choices=EVT_CHOICES,widget=forms.Select(attrs={'class':"form-control"}),required=True)

    class Meta:
        model = Fundraiser
        fields = ['fundraiser_type','title','slug','icon','description','thank_msg','goal_amount','display_name','created_by',
                        'meta_title','meta_description','event_type']
        exclude = ['donation', 'active', 'atype','project', 'company_name']

    def __init__(self,*args,**kwargs):
        super(FundraiserFormBk,self).__init__(*args,**kwargs)
        self.fields["title"].widget=forms.TextInput(attrs={"class":"form-control"})
        self.fields["slug"].widget=forms.TextInput(attrs={"class":"form-control"})
        self.fields["icon"].widget=forms.ClearableFileInput(attrs={"class":"form-upload-btns-wrapper btns"})
        self.fields["fundraiser_type"].widget.attrs["class"]="form-control"
        self.fields["goal_amount"].widget=forms.NumberInput(attrs={"class":"form-control", "readonly":"true"})
        # self.fields["ngo"].widget.attrs["class"]="form-control"
        self.fields["display_name"].widget.attrs["class"]="form-control"
        self.fields["created_by"].widget.attrs["class"]="form-control"
        self.fields["meta_title"].widget.attrs["class"]="form-control"
        self.fields["description"].widget.attrs["class"]="form-control"
        self.fields["thank_msg"].widget.attrs["class"]="form-control"
        self.fields["meta_description"].widget.attrs["class"]="form-control"
 