from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from ckeditor.fields import RichTextField
from django import forms
from mcms.models import *
from Events.models import *
### ****************Models****************
SITE_CHOICES = ( (u'Membership', u'Membership'), (u'main', u'main'), (u'event', u'event'), (u'wishtree', u'wishtree'))
class FaqCategory(Base):
    name = models.CharField(max_length=60)
    is_active = models.BooleanField(default = True)
    added = models.DateTimeField(auto_now_add=True)
    choice = models.CharField(max_length=100,choices=SITE_CHOICES)
    event = models.ForeignKey(Event, blank=True, null=True,on_delete=models.CASCADE)

    class Meta:
        db_table = 'faq_faq_category'

    def __str__(self):
        return self.name

    def get_questions(self):
        return Question.objects.filter(category__id=self.id, is_active=True)

class Question(Base):
    category = models.ForeignKey(FaqCategory,blank=True,null=True,on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    is_active = models.BooleanField(default = True)
    added = models.DateTimeField(auto_now_add=True)


    def get_answer(self):
        return Answer.objects.filter(question__id=self.id)

    def __str__(self):
        return "%s"%(self.question)

class Answer(Base):
    question = models.ForeignKey(Question,blank=True,null=True,on_delete=models.CASCADE)
    answer = RichTextField()
    is_active = models.BooleanField(default = True)
    added = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return "%s"%(self.answer)

### ****************Model Forms****************

class FaqCategoryForm(ModelForm):
    class Meta:
        model = FaqCategory
        exclude = ('is_active','active')

    def __init__(self,*args,**kwargs):
        super(FaqCategoryForm,self).__init__(*args,**kwargs)
        self.fields["name"].widget=forms.TextInput(attrs={"class":"form-control"})
        # self.fields["is_active"].widget=forms.CheckboxInput(attrs={"class":"form-control"})
        self.fields["choice"].widget=forms.Select(attrs={"class":"form-control"},choices=SITE_CHOICES)
        # self.fields["event"].widget.attrs["class"]="form-control" # this is commented to disable event on 24mar

    # class Meta:
    #     model = FaqCategory
    #     exclude = ('is_active',)

class QuestionForm(ModelForm):
    question = forms.CharField(label='Question',max_length=500,widget=forms.Textarea(attrs={'cols': 50, 'rows': 4,"class":'form-control'}),required=True)
    class Meta:
        model = Question
        exclude = ('category', 'is_active','active')

    # question = forms.CharField(label='Question',max_length=500,widget=forms.Textarea(attrs={'cols': 50, 'rows': 4}),required=True)
    # class Meta:
    #     model = Question
    #     exclude = ('category', 'is_active')

class AnswerForm(ModelForm):
    answer=forms.CharField(label='Answer',widget=forms.Textarea(attrs={'cols': 50, 'rows': 4,"class":'form-control'}),required=True)
    class Meta:
        model = Answer
        exclude = ('question', 'is_active','active')


    # class Meta:
    #     model = Answer
    #     exclude = ('question', 'is_active')

