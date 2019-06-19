from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'primero': posts[0]
    })


def post_new(request):
    success = False
    # Cramos el formulario
    form = PostForm()
    # Rellenamos el formulario con el Post del Usuario
    if request.method == 'POST':
        form = PostForm(request.POST)
    # es valido
    if form.is_valid():
        # Guardamos la información del formulario en la base da datos
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        success = True
        return redirect('post_list',)
    return render(request, 'blog/post_edit.html', {
        'form': form,
        'success': success
    })


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list',)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_delete(request, pk):
    Post.objects.filter(pk=pk).delete()
    return redirect('post_list',)
