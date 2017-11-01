from django.shortcuts import render,render_to_response
from django.shortcuts import HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import *
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.utils.decorators import method_decorator
from accounts.forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


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
			context['post_review_list']=PostToReview.objects.filter(status='Pending')
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
	model = PostToReview
	def add_new(request):
		if request.method == "POST":
			form = PostToReviewForm(request.POST or None,request.FILES or None)
			if form.is_valid():
				newpost= form.save(commit=False)
				newpost.image = (request.FILES['image'])
				newpost.no_of_like = 0
				newpost.no_of_comment = 0
				newpost.date = datetime.date.today()
				newpost.status = 'Pending'
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
	fields = ('username', 'first_name', 'last_name', 'email','bio','location','birth_date', 'profile_pic', )
	success_url = reverse_lazy('index')
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'posts/change_password.html', {
        'form': form
    })
@method_decorator(login_required, name='dispatch')
class validate(DetailView):
	def get(self,request,**kwargs):
		postreview=PostToReview.objects.get(id=self.kwargs['pk'])
		if postreview.status=='Pending' and request.user.is_superuser:
			newpost=Post(title=postreview.title,caption=postreview.caption,author=postreview.author,description=postreview.description,image=postreview.image,category=postreview.category,date=postreview.date,no_of_like=postreview.no_of_like,no_of_comment=postreview.no_of_comment)
			newpost.save()
			postreview.status='Accepted'
			postreview.save()
			return HttpResponse("Validation Successful")
		else:
			return HttpResponse("Access Denied")
@method_decorator(login_required, name='dispatch')
class reject(DetailView):
	def get(self, request, **kwargs):
		postreview = PostToReview.objects.get(id=self.kwargs['pk'])
		if postreview.status == 'Pending' and request.user.is_superuser:
			postreview.status = 'Rejected'
			postreview.save()
			return HttpResponse("Rejected")
		else:
			return HttpResponse("Access Denied")
@method_decorator(login_required, name='dispatch')
class ReviewPostList(ListView):
	template_name = 'posts/postlist.html'
	model = Post
	context_object_name = 'post_llist'
	def get_context_data(self, *args, **kwargs):
		context = super(ReviewPostList, self).get_context_data(*args, **kwargs)
		p=PostToReview.objects.filter(author=self.request.user)
		context['review_list']=p.filter(status='Pending')|p.filter(status='Rejected')
		context['post_list'] = Post.objects.filter(author=self.request.user)
		return context
@method_decorator(login_required, name='dispatch')
class CancelReview(DeleteView):
	model = PostToReview
	success_url = reverse_lazy('index')
	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)
@method_decorator(login_required, name='dispatch')
class UpdatePost(UpdateView):
	model=Post
	success_url = reverse_lazy('home')
	fields=('title','caption','author','description','image','category',)
	template_name = 'accounts/posts_update_form.html'
@method_decorator(login_required, name='dispatch')
class DeletePost(DeleteView):
	model = Post
	success_url = reverse_lazy('index')
	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)
@method_decorator(login_required, name='dispatch')
class LikePost(DetailView):
	template_name = 'posts/post_detail.html'
	context_object_name = 'post'
	def get_queryset(self):
		postliked=Post.objects.filter(id=self.kwargs['pk'])
		for update in postliked:
			update.no_of_like+=1
			update.save()
		return postliked
	def get_context_data(self, **kwargs):
		context = super(LikePost, self).get_context_data(**kwargs)
		context['my_post_list'] = Post.objects.filter(author=self.request.user)
		context['category_list'] = Category.objects.all()
		context['comment_list'] = Comment.objects.filter(post=self.kwargs['pk'])
		context['message']={'message':'message'}
		return context
@method_decorator(login_required, name='dispatch')
class UnlikePost(DetailView):
	template_name = 'posts/post_detail.html'
	context_object_name = 'post'
	def get_queryset(self):
		postliked=Post.objects.filter(id=self.kwargs['pk'])
		for update in postliked:
			update.no_of_like-=1
			update.save()
		return postliked
	def get_context_data(self, **kwargs):
		context = super(UnlikePost, self).get_context_data(**kwargs)
		context['my_post_list'] = Post.objects.filter(author=self.request.user)
		context['category_list'] = Category.objects.all()
		context['comment_list'] = Comment.objects.filter(post=self.kwargs['pk'])
		return context