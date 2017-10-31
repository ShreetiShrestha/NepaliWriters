from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

@login_required(login_url='login')
def home(request):
	if request.user.is_superuser:
		return render(request,'posts/home.html',context=None)
	else:
		return HttpResponse("<h1> Hello user </h1>")
# Create your views here.
