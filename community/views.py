from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm, CommentForm
from .models import Post


@login_required
def feed(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('community:feed')
    else:
        form = PostForm()

    posts = Post.objects.all()
    return render(request, 'community/feed.html', {'posts': posts, 'form': form})


@login_required
def view_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('community:view_comments', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'community/view_comments.html', {'post': post, 'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('community:feed')
    return render(request, 'community/delete_post.html', {'post': post})


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('community:feed')
    else:
        form = PostForm(instance=post)
    return render(request, 'community/update_post.html', {'form': form})
