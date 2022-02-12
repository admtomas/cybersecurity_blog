from ast import Try
from django.shortcuts import render,get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#* Index Page view to display all Posts in form of a list
def post_list(request):
    posts = Post.published.all()

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger: #show always first page
        posts = paginator.page(1)
    except EmptyPage: #show last page if out of range
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/post_list.html',{'posts':posts, page:'pages'})

#* Display specific Post instead all of them
def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # redirect to same page and focus on that comment
            return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments,'comment_form':comment_form})

# * Create view for replay
def reply_page(request):
    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input
            reply = form.save(commit=False)

            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+'#'+str(reply.id))

    return redirect('/')
