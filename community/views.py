from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from community.models import Post, Comment
from django.contrib.auth.decorators import login_required
from community.forms import PostForm, CommentForm
from stockAnalysis.models import AnalyzedStock
from django.utils import timezone
from users.models import Profile
import json
from django.db.models import F


def community(request):
    posts = Post.objects.sort_posts_by_time()
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    target_post_ids = [post.id for post in paginated_posts]
    target_posts_with_stock_image = Post.objects.filter(
        id__in=target_post_ids).annotate(
        stock_image=F('analysis_id__stock_image'))

    posts_with_image = []
    for post in target_posts_with_stock_image:
        posts_with_image.append({
            'id': post.id,
            'stock_image': post.stock_image,
        })

    context = {
        'paginated_posts': paginated_posts,
        'serialized_posts': json.dumps(posts_with_image),
        'posts': posts
    }

    return render(request, 'community/community.html', context)


@csrf_exempt
def show_post(request, post_id):
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            content = form.cleaned_data['content']
            publisher = Profile.objects.filter(user_id=request.user).first()
            post = Post.objects.get(pk=post_id)
            Comment.objects.comment_post(post_id=post, content=content, publisher_id=publisher)
            return redirect('post-details', post_id=post_id)

    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.get_all_comments_on_post(post_id=post_id)

    context = {
        'posts': Post.objects.sort_posts_by_time()[:5],
        'post': post,
        'comments': comments,
        'post_chart': post.analysis_id.stock_image
    }
    return render(request, 'community/post-details.html', context)


def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    profile = Profile.objects.filter(user_id=request.user).first()
    is_liked = post.likes.filter(pk=profile.profile_id).exists()
    if is_liked:
        Post.objects.unlike_post(post_id=post_id, profile_id=profile.profile_id)
    else:
        Post.objects.like_post(post_id=post_id, profile_id=profile.profile_id)

    return JsonResponse({'likes': post.likes.count(), 'is_liked': is_liked})


@login_required
def like_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    profile = Profile.objects.filter(user_id=request.user).first()
    is_liked = comment.likes.filter(pk=profile.profile_id).exists()
    if is_liked:
        Comment.objects.unlike_comment(comment_id=comment_id, profile_id=profile.profile_id)
    else:
        Comment.objects.like_comment(comment_id=comment_id, profile_id=profile.profile_id)

    return JsonResponse({'likes': comment.likes.count(), 'is_liked': is_liked})


@login_required
def check_like(request, postId):
    post_id = request.GET.get('post_id')
    profile_id = request.GET.get('profile_id')

    post = Post.objects.get(pk=post_id)

    liked = post.likes.filter(pk=profile_id).exists()

    return JsonResponse({'liked': liked})


@login_required
def check_comment_like(request, commentId):
    comment_id = request.GET.get('comment_id')
    profile_id = Profile.objects.get(user_id=request.user).profile_id

    comment = Comment.objects.get(pk=comment_id)

    liked = comment.likes.filter(pk=profile_id).exists()

    return JsonResponse({'liked': liked})


@login_required
def delete_comment(request, post_id, comment_id):
    profile = Profile.objects.filter(user_id=request.user).first()
    Comment.objects.delete_comment(comment_id=comment_id, profile_id=profile.profile_id)

    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.get_all_comments_on_post(post_id=post_id)
    context = {'posts': Post.objects.all().values, 'post': post, 'comments': comments}

    return render(request, 'community/post-details.html', context)


@login_required
def delete_post(request, post_id):
    profile = Profile.objects.filter(user_id=request.user).first()
    Post.objects.delete_post(post_id=post_id, profile_id=profile.profile_id)

    return community(request=request)


def create_post(analyzed_stock, description, title):
    (post, created) = Post.objects.get_or_create(
        analysis_id=analyzed_stock,
        description=description,
        title=title,
        time=timezone.now()
    )

    return created
