from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.groups, name='groups'),
    url(r'^(?P<group_id>[0-9]+)/$',views.editGroup, name='group'),

]
