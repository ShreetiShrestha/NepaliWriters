from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import *
from django.contrib.auth import login, authenticate
from accounts.forms import SignUpForm
from django.views.generic import ListView
# Create your views here.
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('/main/')

class MainPage(ListView):
    model = Category
    template_name = 'accounts/index.html'
    context_object_name = 'category_list'
    def get_context_data(self, *args, **kwargs):
        context = super(MainPage, self).get_context_data(*args, **kwargs)
        context['post_list'] = Post.objects.order_by('no_of_like')
        context['user_list'] = User.objects.all()[:5]
        return context



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            image=(request.FILES['profile_pic'])
            user = form.save(commit=False)
            user.profile_pic=request.FILES['profile_pic']
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
