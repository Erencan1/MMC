from django.conf.urls import url
from .views import index1, index2

urlpatterns = [
    url(r'^$', index1),
    url(r'^switch/$', index2),
]