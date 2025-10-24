from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import PostForm, CommentForm, MessageForm
from .models import Post, Message
from accounts.models import User

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



@login_required
def inbox(request):
    # Get all users except current user
    users = User.objects.exclude(id=request.user.id)

    # Get selected conversation
    selected_user_id = request.GET.get('user')
    conversation = []
    selected_user = None

    if selected_user_id:
        selected_user = get_object_or_404(User, id=selected_user_id)
        conversation = Message.objects.filter(
            Q(sender=request.user, receiver=selected_user) |
            Q(sender=selected_user, receiver=request.user)
        )
        # Mark as read
        Message.objects.filter(sender=selected_user, receiver=request.user, is_read=False).update(is_read=True)

    # Send message
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver_id')
        if content and receiver_id:
            Message.objects.create(
                sender=request.user,
                receiver_id=receiver_id,
                content=content
            )
            return redirect(f'/community/inbox/?user={receiver_id}')

    return render(request, 'community/inbox.html', {
        'users': users,
        'conversation': conversation,
        'selected_user': selected_user
    })
