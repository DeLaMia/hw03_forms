from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, Group, User
from .forms import PostForm
from django.shortcuts import redirect


LAST_10_POSTS: int = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, LAST_10_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, LAST_10_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    paginator = Paginator(post_list, LAST_10_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = post_list.count()
    context = {
        'author': author,
        'post_count': post_count,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_more = Post.objects.get(pk=post_id)
    post_count = (post_more.author).posts.count()
    context = {
        'post_more': post_more,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('posts:profile', request.user.username)
        return render(request, 'posts/post_create.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    if request.method == "POST":
        if form.is_valid:
            form.save()
            return redirect('posts:post_detail', post_id)
    context = {'form': form, 'is_edit': True, 'post': post}
    return render(request, 'posts/post_create.html', context)
