from django.shortcuts import render
from mcms.models import IndividualActivation
from django.contrib.auth.models import User
# Create your views here.
def useractivation(request):
    user = 0
    activation_key = request.GET.get('activation_key')
    try:
        useractobj = IndividualActivation.objects.get(activation_key=activation_key)
        if not useractobj.is_active:
            user = User.objects.get(username=useractobj.user.username)
            user.is_active=True
            user.save()
            useractobj.is_active=True
            useractobj.save()
            msg = "your account is activated"
            return render(request,'frontend_templates/user_activation.html',locals())

        else:
            msg = "Your account is already activated"
            user = User.objects.get(username=useractobj.user.username)
            return render(request,'frontend_templates/user_activation.html',locals())

    except:
        return render(request,'frontend_templates/user_activation.html',locals())


def get_active_events():
    event_type = ['Marathon']
    return Event.objects.filter(active=True, accept_donation=True, event_type__in=event_type).exclude(slug="edudaan")
