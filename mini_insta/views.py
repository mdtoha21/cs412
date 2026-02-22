from django.views.generic import ListView, DetailView,CreateView
from .models import Profile,Post,Photo
from .forms import CreatePostForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
class ProfileListView(ListView):
    '''Define a view class to show all mini_insta profiles'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"



class ProfileDetailView(DetailView):
    '''Define a view class to show a singlr mini_insta profiles'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    model=Post
    template_name="mini_insta/show_post.html"
    context_object_name="post"


class CreatePostView(CreateView):
    '''Allow users to create a new Post associated with a specific Profile.
'''
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"


    def get_context_data(self, **kwargs):

        '''Add the Profile object to the context data
        so the form knows which Profile this Post belongs to.'''

        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context


    def form_valid(self, form):
        ''' Attaches the Post to the correct Profile and creates an associated Photo.'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        post = form.save(commit=False)
        post.profile = profile
        post.save()

 
        image_url = self.request.POST.get('image_url')
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)
        
        self.object = post

        return super().form_valid(form)
    
    def get_success_url(self):
         '''     Redirect the user to the new Post's detail page after creation.'''


         return reverse('show_post', args=[self.object.pk])