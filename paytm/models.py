from django.db import models
from django.conf import settings
from mcms.models import *
from django.utils import timezone
# Create your models here.

class PaytmHistory(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_payment_paytm', blank=True, null=True,on_delete=models.CASCADE)
    ORDERID = models.CharField('ORDER ID', max_length=300)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField('TXN ID', max_length=100)
    BANKTXNID = models.CharField('BANK TXN ID', null=True, blank=True, max_length=100)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    class Meta:
        app_label = 'paytm'

    def __str__(self):
        return self.STATUS
