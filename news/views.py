from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from accounts.utils import DEFAULT_AVATAR_PATH
from newsletter.settings import NEWS_PAGINATE_BY
from .models import Article, Comment
from .forms import ArticleForm, CommentForm


def get_article_async(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        if slug:
            article = Article.objects.filter(slug=slug)
            if article:
                skip = request.POST.get('skip')
                if skip and skip.isnumeric():
                    skip_n = int(skip)
                    return JsonResponse({'is_ok': True, 'content': article[0].content.split(' ', skip_n)[skip_n]})
                return JsonResponse({'is_ok': True, 'content': article[0].content})
    return JsonResponse({'is_ok': False})


def articles_list(request):
    articles = Article.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(articles, NEWS_PAGINATE_BY)
    articles = paginator.get_page(page)
    context = {'articles': articles}
    return render(request, 'news/list.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
def articles_my_list(request):
    articles = Article.objects.filter(author__user__username=request.user.username)
    page = request.GET.get('page')
    paginator = Paginator(articles, NEWS_PAGINATE_BY)
    articles = paginator.get_page(page)
    context = {'articles': articles}
    return render(request, 'news/my_list.html', context)


def search_list(request):
    q = request.GET.get('q')
    if q:
        articles = Article.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(author__fio_name__icontains=q)
        )
    else:
        articles = Article.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(articles, NEWS_PAGINATE_BY)
    articles = paginator.get_page(page)
    context = {'articles': articles, 'q': q}
    return render(request, 'news/search.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = Comment.objects.filter(article=article)
    comment_form = None
    if request.user.is_authenticated:
        comment_form = CommentForm()
    context = {'article': article, 'comments': comments, 'comment_form': comment_form,
               'default_avatar_path': DEFAULT_AVATAR_PATH}
    return render(request, 'news/detail.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
def comment_create(request, slug):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user.profile
            comment.article = Article.objects.get(slug=slug)
            comment.save()
    return redirect('news:detail', slug)


@login_required(login_url=reverse_lazy('accounts:login'))
def comment_delete(request, slug, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user.is_superuser or comment.author.user == request.user:
            comment.delete()
        else:
            raise PermissionDenied
    return redirect('news:detail', slug)


@login_required(login_url=reverse_lazy('accounts:login'))
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.profile
            article.save()
            return redirect('news:detail', article.slug)
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'news/create.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.user.is_superuser or article.author.user == request.user:
        form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('news:detail', slug)
        context = {'article': article, 'form': form}
        return render(request, 'news/edit.html', context)
    else:
        raise PermissionDenied


@login_required(login_url=reverse_lazy('accounts:login'))
def article_delete(request, slug):
    if request.method == 'POST':
        article = get_object_or_404(Article, slug=slug)
        if request.user.is_superuser or article.author.user == request.user:
            article.delete()
        else:
            raise PermissionDenied
    return redirect('news:list')
