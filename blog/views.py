from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.http import HttpResponseRedirect

from django.views.generic import ListView
from taggit.models import Tag

from django.core.mail import send_mail

from .models import Post, Category, Comment
from .forms import EmailPostForm, CommentForm


def home(request):
    recent_posts = Post.published.all()[:3]
    featured_post = Post.objects.filter(is_featured=True)[:5]
    context = {
        'recent_posts': recent_posts,
        'featured_post': featured_post,
    }
    return render(request=request, template_name='blog/post/home.html', context=context)


def post_list(request, category_id=None, tag_slug=None):
    featured_post = Post.objects.filter(is_featured=True)[:1]
    post_list = Post.published.all()
    recent_post = Post.published.all()[:3]
    category = None
    tag = None
    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        post_list = post_list.filter(category=category)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        paged_posts = paginator.page(page_number)
    except PageNotAnInteger:
        paged_posts = paginator.page(1)
    except EmptyPage:
        paged_posts = paginator.page(paginator.num_pages)

    context = {
        'featured_post': featured_post,
        'paged_posts': paged_posts,
        'tag': tag,
        'category': category,
        'recent_post': recent_post,
    }
    return render(request=request, template_name='blog/post/post_list.html', context=context)


def post_detail(request, slug=None):
    single_post = get_object_or_404(
        Post,
        slug=slug,
        status=Post.Status.PUBLISHED
    )

    # comments = single_post.comments.filter(active=True)
    # form = CommentForm()

    # Список схожих постів
    post_tags_ids = single_post.tags.values_list('pk', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(pk=single_post.pk)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('same_tags', 'publish')[:2]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = single_post
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(f'{request.path_info}#comments')
    else:
        comment_form = CommentForm()

    # Comments
    comments = Comment.objects.filter(post=single_post)
    comment_count = comments.count()

    context = {
        'single_post': single_post,
        'comment_form': comment_form,
        'comment_count': comment_count,
        'comments': comments,
        # 'form': form,
        'similar_posts': similar_posts,
    }
    return render(request=request, template_name='blog/post/post_detail.html', context=context)


def post_share(request, pk):
    post = get_object_or_404(
        Post,
        pk=pk,
        status=Post.Status.PUBLISHED
    )

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()

    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request=request, template_name='blog/post/post_share.html', context=context)




