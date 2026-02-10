from django.shortcuts import render  # ← NEW: Import render!
from django.http import HttpResponse
from .models import Post

# Add this line with your other imports:
from .forms import PostForm  

# Your imports should look like:
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from .forms import PostForm  # ← NEW LINE
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404

def post_list(request):
    """Show blog posts - users see only their own, admin sees all"""
    if request.user.is_staff or request.user.is_superuser:
        # Admin sees ALL posts
        posts = Post.objects.all().order_by('-published_date')
    elif request.user.is_authenticated:
        # Regular users see only THEIR posts
        posts = Post.objects.filter(author=request.user).order_by('-published_date')
    else:
        # Guests see only published posts
        posts = Post.objects.filter(is_published=True).order_by('-published_date')
    
    context = {
        'posts': posts,
        'page_title': 'Blog Posts',
        'user': request.user,
    }
    return render(request, 'blog/post_list.html', context)

@login_required
def post_unpublished(request):
    """Show unpublished posts - users see only their own, admin sees all"""
    if request.user.is_staff or request.user.is_superuser:
        # Admin sees ALL drafts
        posts = Post.objects.filter(is_published=False).order_by('-published_date')
        page_title = "All Draft Posts (Admin View)"
    elif request.user.is_authenticated:
        # Regular users see only THEIR drafts
        posts = Post.objects.filter(
            author=request.user, 
            is_published=False
        ).order_by('-published_date')
        page_title = f"Your Draft Posts ({request.user.username})"
    else:
        # Guests shouldn't see drafts - redirect to login
        return redirect('login')
    
    context = {
        'posts': posts,
        'page_title': page_title,
    }
    return render(request, 'blog/post_unpublished.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)

# LINE 1: Define a view function called post_create
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set current user as author
            post.save()
            messages.success(request, "✅ Post created successfully!")
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create New Post'})

@login_required
def post_edit(request,post_id):
    post=get_object_or_404(Post,id=post_id)
     # Check if user owns this post OR is admin
    if post.author != request.user and not request.user.is_staff:
        raise Http404("You don't have permission to edit this post.")
    if request.method=='POST':
        form=PostForm(request.POST,instance=post)
        if form.is_valid:
            form.save()
            return redirect('post_detail',post_id=post.id)
    else:
        form=PostForm(instance=post)
    context={
        'form':form,
        'title':"Edit post",
        'post':post
    }          
    return render(request,'blog/post_form.html',context)

@login_required
def post_delete(request, post_id):
    """Delete a blog post with confirmation"""
    post = get_object_or_404(Post, id=post_id)
    # Check if user owns this post OR is admin
    if post.author != request.user and not request.user.is_staff:
        raise Http404("You don't have permission to delete this post.")
    if request.method == 'POST':
        # User confirmed deletion
        post.delete()  # ← Just one line deletes from database!
        return redirect('post_list')  # Go back to blog list
    
    # Show confirmation page (GET request)
    context = {
        'post': post,
        'title': 'Delete Post'
    }
    return render(request, 'blog/post_confirm_delete.html', context)

