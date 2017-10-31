from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^adminview/$',views.Adminview.as_view(), name='adminview'),
    url(r'^userview/$',views.Userview.as_view(), name='userview'),
    url(r'^post/(?P<pk>\d+)$', views.PostDetail.as_view(), name='post_detail'),
    url(r'^post/add/$', views.PostToReviewCreate.add_new, name='post_add'),
    url(r'^reviewpost/(?P<pk>\d+)$', views.ReviewPostDetail.as_view(), name='review_post_detail'),
    url(r'^profile/(?P<pk>\d+)$', views.UserProfile.as_view(), name='userprofile'),
    url(r'^profile/update/(?P<pk>\d+)$', views.UpdateUserProfile.as_view(), name='updateprofile'),
]
