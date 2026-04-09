from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.

from .models import Post, Hashtag, Location, Participant
from .forms import PostForm, Commentform

def home(request):
    filter_status = request.GET.get('status')

    if filter_status == 'recruiting':
        posts = Post.objects.filter(status='모집중').order_by('-created_at')
        
    else:
        posts = Post.objects.all().order_by('-created_at')
        
    return render(request, 'home.html', {'posts': posts})

def detail(request, post_id):

 post_detail=get_object_or_404(Post, pk=post_id)
 post_hashtag=post_detail.hashtag.all()

 return render(request, 'detail.html', {'post': post_detail, 'hashtage': post_hashtag})

def new(request):
    form=PostForm()
    return render(request, 'new.html', {'form': form})


 

def create(request):
  form=PostForm(request.POST, request.FILES)

  if form.is_valid():

    new_SplitIt=form.save(commit=False)
    new_SplitIt.save()
    hashtags=request.POST['hashtags']
    hashtag_list=hashtags.split(', ')


    for tag in hashtag_list:

        tag = tag.strip()

        new_hashtag=Hashtag.objects.get_or_create(hashtag=tag)

        new_SplitIt.hashtag.add(new_hashtag[0])

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


def add_comment(request, post_id):

    SplitIt = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = Commentform(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = SplitIt

            comment.save()

            return redirect('SplitIt:detail', post_id)
    else:
        form = Commentform()

    return render(request, 'add_comment.html', {'form': form})


def join_post(request, post_id):
   post = get_object_or_404(Post, pk=post_id)

   if request.method =='POST':
      nickname = request.POST.get('nickname')

      if nickname and post.participants.count()<post.target_headcount:
         Participant.objects.create(post=post, nickname=nickname, menu='참여완료')

      return redirect('SplitIt:detail', post_id=post.id)