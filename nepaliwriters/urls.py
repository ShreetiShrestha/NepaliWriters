from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from accounts.forms import LoginForm
from django.contrib.auth import views as auth_views
from accounts import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('accounts.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^home/', include('posts.urls'),name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^main/', views.MainPage.as_view(), name='mainpage'),
    url(r'^tinymce/', include('tinymce.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
