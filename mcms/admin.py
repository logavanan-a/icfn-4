from django.contrib import admin
from NGO.models import *
from Events.models import *
from mcms.models import *
from faq.models import *
from wishtree.models import *
# Register your models here.
# admin.site.register(NGO)

# class NGOAdmin(admin.ModelAdmin):
#     fields = ('name', 'icon')

class NGOAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	exclude = ('project','ngo_keywords','we_are_on','secondary_focus')


class FundraiserAdmin(admin.ModelAdmin):
	search_fields = ('company_name','title')
	exclude = ('donation',)


class DonationAdmin(admin.ModelAdmin):
	search_fields = ('first_name',)

admin.site.register(NGO, NGOAdmin)
admin.site.register(ReachOutHeading)
admin.site.register(ReachOutProgram)
admin.site.register(Event)
admin.site.register(EventAwards)
admin.site.register(OfflineDonation)
admin.site.register(EventAboutUs)
admin.site.register(EventBanners)
admin.site.register(EventContactUs)
admin.site.register(EventRunReport)
admin.site.register(Staff)
admin.site.register(FundraiserType)
admin.site.register(Fundraiser,FundraiserAdmin)
admin.site.register(WishTree)
admin.site.register(WishtreeCampaigns)
admin.site.register(AnnualReport)
admin.site.register(Donation,DonationAdmin)
admin.site.register(DuplicateCorporates)
admin.site.register(Campaign)
admin.site.register(HomePageSpeak)
admin.site.register(AccrossTheCountry)
admin.site.register(DashboardChartWidgets)
admin.site.register(UserProfile)
admin.site.register(EventNgoDescription)
admin.site.register(HomePageMediaContent)
admin.site.register(ShareDetails)
admin.site.register(TopEventAwards)
admin.site.register(UserDetails)
admin.site.register(Address)
admin.site.register(Article)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(FaqCategory)
admin.site.register(Contactus)
admin.site.register(OurInitiatives)
admin.site.register(OurEvents)
admin.site.register(DonationReceipts)
admin.site.register(EventConfig)
admin.site.register(EventExtended)
admin.site.register(WishtreeNgo)
admin.site.register(Wish)
admin.site.register(WishtreeImage)
admin.site.register(DoantionMailer)
admin.site.register(Salutations)
admin.site.register(Section)
admin.site.register(NgoCommunication)
admin.site.register(EventAmountDeduction)
admin.site.register(Link)
admin.site.register(FundraiserTypeDetails)


