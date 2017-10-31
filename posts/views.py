from django.shortcuts import render,render_to_response
from django.shortcuts import HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import *
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.utils.decorators import method_decorator

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


