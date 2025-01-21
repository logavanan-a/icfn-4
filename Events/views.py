from django.shortcuts import render

from django.shortcuts import render
from NGO.models import *
from django.db.models import Q
from watson import search as watson

import time
from Events.module import *
# Create your views here.

