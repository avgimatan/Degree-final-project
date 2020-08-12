from django.conf.urls import url

from . import views

app_name = 'avatars'

urlpatterns = [
    # url(r"^$", views.AvatarList.as_view(), name="all"),
    url(r"new/$", views.CreateAvatar.as_view(), name="create"),
    url(r"by/(?P<username>[-\w]+)/$", views.UserAvatar.as_view(), name="for_user"),
    # url(r"^search/in/(?P<slug>[-\w]+)/$", views.SingleAvatar.as_view(), name="single"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$", views.AvatarDetail.as_view(), name="single"),
    url(r"delete/(?P<pk>\d+)/$", views.DeleteAvatar.as_view(), name="delete"),
]
