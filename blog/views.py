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
def post_list(request):
    # Get data from database
    posts=Post.objects.filter(is_published=True)
    # Prepare context (data for template)
    context = { # This is a dictionary of data we send to the template
        'posts': posts,
        'page_title': 'Published Blog Posts',
    }
    return render(request, 'blog/post_list.html', context)

def post_unpublished(request):
    posts=Post.objects.filter(is_published=False)
    context={
        'posts':posts,
        'page_title':'Unpublished Blog Posts',
    }
    return render(request,'blog/post_unpublished.html',context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)

# LINE 1: Define a view function called post_create
def post_create(request):
    # Think: "This function handles creating new posts"
    
    # LINE 2: Check if user submitted the form
    if request.method == 'POST':
        # Think: "User clicked SAVE button"
        
        # LINE 3: Create form with submitted data
        form = PostForm(request.POST)
        # Think: "Fill form with what user typed"
        
        # LINE 4: Check if data is valid
        if form.is_valid():
            # Think: "No errors in form data"
            
            # LINE 5: Save to database and get post object
            post = form.save()
            # Think: "Create new Post in database"
            messages.success(request, f"✅ Post '{post.title}' created successfully!")
            # LINE 6: Redirect to the new post's page
            return redirect('post_detail', post_id=post.id)
            # Think: "Go to /blog/1/ to see the new post"
        else:
            message.error(request,"❌ Please fix the errors below.")
    # LINE 7: If NOT POST (user just opened page)
    else:
        # Think: "User clicked 'New Post' link"
        
        # LINE 8: Show empty form
        form = PostForm()
        # Think: "Create blank form"
    
    # LINE 9: Prepare data for template
    context = {'form': form, 'title': 'Create New Post'}
    # Think: "Package form and title for HTML page"
    
    # LINE 10: Show the form page
    return render(request, 'blog/post_form.html', context)
    # Think: "Display the form HTML with our data"

def post_edit(request,post_id):
    post=get_object_or_404(Post,id=post_id)
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

def post_delete(request, post_id):
    """Delete a blog post with confirmation"""
    post = get_object_or_404(Post, id=post_id)
    
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