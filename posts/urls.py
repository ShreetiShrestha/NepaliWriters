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
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^validate/(?P<pk>\d+)$', views.validate.as_view(), name='validate_post'),
    url(r'^reject/(?P<pk>\d+)$', views.reject.as_view(), name='reject_post'),
    url(r'^update/(?P<pk>\d+)$', views.UpdatePost.as_view(), name='update_post'),
    url(r'^delete/(?P<pk>\d+)$', views.DeletePost.as_view(), name='delete_post'),
    url(r'^myvalidation/$', views.ReviewPostList.as_view(), name='my_validation_list'),
    url(r'^cancelmyvalidation/(?P<pk>\d+)$', views.CancelReview.as_view(), name='cancel_my_validation'),
    url(r'^like/(?P<pk>\d+)$', views.LikePost.as_view(), name='like_post'),
    url(r'^unlike/(?P<pk>\d+)$', views.UnlikePost.as_view(), name='unlike_post'),
    url(r'^comment/(?P<pk>\d+)$', views.CommentPost.as_view(), name='post_comment'),
    url(r'^category/posts/(?P<pk>\d+)$', views.CategoryPostList.as_view(), name='category_listing'),

]
