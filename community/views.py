from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PostForm
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