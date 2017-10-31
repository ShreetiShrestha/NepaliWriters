from django.shortcuts import render,render_to_response
from django.shortcuts import HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import *
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.utils.decorators import method_decorator
from accounts.forms import *
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

@login_required(login_url='login')
def home(request):
	if request.user.is_superuser:
		return redirect('adminview')
	else:
		return redirect('userview')

@method_decorator(login_required, name='dispatch')
class Adminview(ListView):
	model = Post
	template_name = 'posts/home_admin.html'
	context_object_name = 'post_list'
	def get_context_data(self, *args, **kwargs):

		if self.request.user.is_superuser:
			context = super(Adminview, self).get_context_data(*args, **kwargs)
			context['category_list'] = Category.objects.order_by('no_of_post')
			context['post_review_list']=PostToReview.objects.all()
			return context
		else:
			context=None
			return context

@method_decorator(login_required, name='dispatch')
class Userview(ListView):
	model = Category
	template_name = 'posts/home_user.html'
	context_object_name = 'category_list'
	def get_context_data(self, *args, **kwargs):
		context = super(Userview, self).get_context_data(*args, **kwargs)
		context['post_list'] = Post.objects.all()[:6]
		context['my_post_list']=Post.objects.filter(author=self.request.user)
		context['usercontext']=User.objects.filter(username=self.request.user)
		return context


class PostDetail(DetailView):
	model = Post
	template_name = 'posts/post_detail.html'
	context_object_name = 'post'

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetail, self).get_context_data(*args, **kwargs)
		context['my_post_list'] = Post.objects.filter(author=self.request.user)
		context['category_list'] = Category.objects.all()
		context['comment_list'] = Comment.objects.filter(post=self.kwargs['pk'])
		return context

@method_decorator(login_required, name='dispatch')
class ReviewPostDetail(DetailView):
	model = PostToReview
	template_name = 'posts/post_review_detail.html'
	context_object_name = 'post'

	def get_context_data(self, *args, **kwargs):
		context = super(ReviewPostDetail, self).get_context_data(*args, **kwargs)
		return context

@method_decorator(login_required, name='dispatch')
class PostToReviewCreate(CreateView):
	def add_new(request):
		if request.method == "POST":
			form = PostToReviewForm(request.POST or None,request.FILES or None)
			if form.is_valid():
				newpost= form.save(commit=False)
				newpost.image = (request.FILES['image'])
				newpost.no_of_like = 0
				newpost.no_of_comment = 0
				newpost.date = datetime.date.today()
				newpost.status = False
				newpost.save()
				return render(request,'thankyou.html',context=None)
		else:
			form = PostToReviewForm()
		return render(request, 'accounts/post_form.html', {'form': form})

class UserProfile(DetailView):
	model = User
	template_name = 'posts/user_detail.html'
	context_object_name = 'usercontext'
	def get_context_data(self, *args, **kwargs):
		context = super(UserProfile, self).get_context_data(*args, **kwargs)
		context['my_post_list'] = Post.objects.filter(author=self.kwargs['pk'])
		return context
@method_decorator(login_required, name='dispatch')
class UpdateUserProfile(UpdateView):
	model = User
	template_name = 'posts/profile.html'
	fields = ('username', 'first_name', 'last_name', 'email', 'password','bio','location','birth_date', 'profile_pic', )
	success_url = reverse_lazy('index')


