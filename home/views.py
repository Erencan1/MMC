from django.shortcuts import render
from django.http import HttpResponse
from .models import Person, MMC


def index1(request):
    p = Person()
    p.name = 'New Person'
    p.save()
    return HttpResponse('New Person in %s' % Person._mmc_db_name)
    # return render(request, 'htmlfiles/index.html')


def index2(request):
    if Person._mmc_db_name == 'DB2':
        MMC.setdb('DB3')(Person)
    else:
        MMC.setdb('DB2')(Person)
    return HttpResponse('Person DB Router has been changed to %s' % Person._mmc_db_name)
    # return render(request, 'htmlfiles/index.html')