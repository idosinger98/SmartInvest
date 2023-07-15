from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from community.models import Post, Comment
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


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})
