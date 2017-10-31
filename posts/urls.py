from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^adminview/$',views.Adminview.as_view(), name='adminview'),
    url(r'^userview/$',views.Userview.as_view(), name='userview'),
    url(r'^post/(?P<pk>\d+)$', views.PostDetail.as_view(), name='post_detail'),

]
