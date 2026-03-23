from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.

from .models import Post
from .forms import PostForm

def home(request):
    filter_status = request.GET.get('status')

    if filter_status == 'recruiting':
        posts = Post.objects.filter(status='모집중').order_by('-created_at')
        
    else:
        posts = Post.objects.all().order_by('-created_at')
        
    return render(request, 'home.html', {'posts': posts})

def detail(request, post_id):

 post_detail=get_object_or_404(Post, pk=post_id)

 return render(request, 'detail.html', {'post': post_detail})

def new(request):
    form=PostForm()
    return render(request, 'new.html', {'form': form})


 

def create(request):
  form=PostForm(request.POST, request.FILES)

  if form.is_valid():

    new_SplitIt=form.save(commit=False)

    new_SplitIt.save()

    return redirect('SplitIt:detail', new_SplitIt.id)

  return redirect('SplitIt:home')

 

def delete(request, post_id):

 delete_SplitIt = get_object_or_404(Post, pk=post_id)

 delete_SplitIt.delete()

 return redirect('SplitIt:home')
def update_page(request, post_id):

 update_SplitIt = get_object_or_404(Post, pk=post_id)

 return render(request, 'update.html', {'update_SplitIt': update_SplitIt})


def update_post(request, post_id):

 update_SplitIt = get_object_or_404(Post, pk=post_id) 

 update_SplitIt.title = request.POST['title']

 update_SplitIt.content = request.POST['content']

 update_SplitIt.save()

 return redirect('SplitIt:home')

def complete_recruitment(request, post_id):
  
    post = Post.objects.get(id=post_id)
    
   
    post.status = '모집완료'
    

    post.save()
    
  
    return redirect('SplitIt:detail', post.id)