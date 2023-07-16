from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from community.models import Post, Comment
from users.models import Profile
from django.http import JsonResponse


def community(request):
    posts = Post.objects.sort_posts_by_popularity()
    context = {'posts': posts}
    return render(request, 'community/community.html', context)


def show_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.get_all_comments_on_post(post_id=pk)
    context = {'posts': Post.objects.all().values, 'post': post, 'comments': comments}
    return render(request, 'community/post-details.html', context)


# @csrf_exempt
# def like_post(request):
#     if request.method == 'POST':
#         post_id = request.POST.get('post_id')
#         if post_id:
#             post = Post.objects.get(id=post_id)
#             post.like_post()
#             return JsonResponse({'success': True})
#     return JsonResponse({'success': False})


def like_post(request, post_id, profile_id):
    post = Post.objects.get(pk=post_id)
    is_liked = post.likes.filter(pk=profile_id).exists()
    if is_liked:
        Post.objects.unlike_post(post_id=post_id, profile_id=profile_id)
    else:
        Post.objects.like_post(post_id=post_id, profile_id=profile_id)

    return JsonResponse({'likes': post.likes.count(), 'is_liked': is_liked})


def like_comment(request, comment_id, profile_id):
    comment = Comment.objects.get(pk=comment_id)
    is_liked = comment.likes.filter(pk=profile_id).exists()
    if is_liked:
        Comment.objects.unlike_comment(comment_id=comment_id, profile_id=profile_id)
    else:
        Comment.objects.like_comment(comment_id=comment_id, profile_id=profile_id)

    return JsonResponse({'likes': comment.likes.count(), 'is_liked': is_liked})


def check_like(request, postId):
    post_id = request.GET.get('post_id')
    profile_id = request.GET.get('profile_id')

    post = Post.objects.get(pk=post_id)
    profile = Profile.objects.get(pk=profile_id)

    liked = post.likes.filter(pk=profile_id).exists()

    return JsonResponse({'liked': liked})


def check_comment_like(request, commentId):
    comment_id = request.GET.get('comment_id')
    profile_id = request.GET.get('profile_id')

    comment = Comment.objects.get(pk=comment_id)
    profile = Profile.objects.get(pk=profile_id)

    liked = comment.likes.filter(pk=profile_id).exists()

    return JsonResponse({'liked': liked})
