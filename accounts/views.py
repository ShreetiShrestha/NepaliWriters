from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import login, authenticate
from accounts.forms import SignUpForm
# Create your views here.
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
def index(request):
    return render(request,'accounts/index.html',context=None)
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
