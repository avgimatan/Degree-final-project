from django.conf.urls import url

from . import views

app_name = 'search'

urlpatterns = [
    url(r"^$", views.SearchChoose.as_view(), name="choose"),
    url(r"userdashboard/$", views.UserDashboard.as_view(), name="user_dashboard"),
    url(r"keyworddashboard/$", views.KeywordDashboard.as_view(), name="keyword_dashboard")

]
